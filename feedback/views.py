from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from upload.models import UserUpload
from .models import FeedbackResult
from .nlp_processing import clip_audio, stt_audio, calculate_accuracy, analyze_speed
from .video_processing import VideoProcessor
import os
from moviepy import AudioFileClip

class FeedbackProcessingView(APIView):
    def post(self, request, upload_id):
        try:
            # 1. 업로드된 파일 가져오기
            upload = UserUpload.objects.get(id=upload_id, user=request.user)
            if upload.processed:
                return Response({'message': 'File already processed'}, status=400)

            ### STEP 1: NLP 처리 ###
            try:
                # (1) 오디오 파일 클립으로 분할
                clip_folder = os.path.join(settings.MEDIA_ROOT, "clips", str(upload.id))
                clip_audio(upload.processed_audio.path, clip_folder)

                # (2) STT 처리
                stt_text = stt_audio(os.path.join(clip_folder, "clip_1.mp3"))
                accuracy = calculate_accuracy(upload.script, stt_text)

                # (3) 발화 속도 계산
                audio_duration = AudioFileClip(upload.processed_audio.path).duration
                syllables_per_second, _ = analyze_speed(stt_text, audio_duration)
            except Exception as e:
                return Response({'error': f'NLP processing failed: {str(e)}'}, status=500)

            ### STEP 2: 영상 처리 ###
            try:
                # (1) 비디오 파일 행동 분석
                video_processor = VideoProcessor(source=upload.processed_video.path)
                video_results = video_processor.process_video()
            except Exception as e:
                return Response({'error': f'Video processing failed: {str(e)}'}, status=500)

            ### STEP 3: 결과 저장 ###
            feedback = FeedbackResult.objects.create(
                upload=upload,
                accuracy=accuracy,
                syllables_per_second=syllables_per_second,
                speed="fast" if syllables_per_second > 5.16 else "slow",
                um_count=stt_text.count("음"),
                uh_count=stt_text.count("어"),
                geu_count=stt_text.count("그"),
                bad_gesture_count=video_results["bad_gesture_count"],
                good_gesture_count=video_results["good_gesture_count"],
                standing_on_one_leg_count=video_results["standing_on_one_leg_count"]
            )

            # 처리 완료 상태 업데이트
            upload.processed = True
            upload.save()

            return Response({
                'message': 'Feedback processing completed',
                'feedback_id': feedback.id
            }, status=200)

        except UserUpload.DoesNotExist:
            return Response({'error': 'File not found'}, status=404)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=500)