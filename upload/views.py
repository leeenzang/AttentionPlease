import os
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils.timezone import now
from .models import UserUpload
from .serializers import UserUploadSerializer

class FileUploadView(APIView):
    def post(self, request):
        # Step 1: 한 사용자당 하나의 파일만 허용
        UserUpload.objects.filter(user=request.user).delete()

        # Step 2: 파일 타입 제한
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.mp4'):
            return Response({'error': 'Only .mp4 files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: 파일과 스크립트 저장
        script = request.data.get('script')  # 스크립트를 요청에서 추출
        if not script:
            return Response({'error': 'Script is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserUploadSerializer(data=request.data)
        if serializer.is_valid():
            upload = serializer.save(user=request.user, script=script)  # 스크립트 저장

            try:
                # Step 4: mp4 → 오디오(M4A) 변환
                audio_output_path = os.path.join(settings.MEDIA_ROOT, f'processed_audio/{upload.id}.m4a')
                subprocess.run(
                    f"ffmpeg -i {upload.file.path} -vn -acodec copy {audio_output_path}",
                    shell=True, check=True
                )
                upload.processed_audio = f'processed_audio/{upload.id}.m4a'

                # Step 5: mp4 그대로 영상팀용으로 복사
                video_output_path = os.path.join(settings.MEDIA_ROOT, f'processed_video/{upload.id}.mp4')
                subprocess.run(
                    f"ffmpeg -i {upload.file.path} -c copy {video_output_path}",
                    shell=True, check=True
                )
                upload.processed_video = f'processed_video/{upload.id}.mp4'

                # Step 6: 처리 완료 시간 저장
                upload.processed_at = now()
                upload.save()

                return Response({
                    'message': 'File uploaded and processed successfully!',
                    'file_id': upload.id,
                    'processed_audio': upload.processed_audio.url,
                    'processed_video': upload.processed_video.url,
                    'script': upload.script
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                upload.delete()  # 변환 실패 시 데이터 삭제
                return Response({'error': f'File processing failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)