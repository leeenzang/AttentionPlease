from django.db import models
from upload.models import UserUpload

class FeedbackResult(models.Model):
    # NLP 분석 결과
    upload = models.OneToOneField(UserUpload, on_delete=models.CASCADE, related_name='feedback')
    accuracy = models.FloatField(null=True, blank=True)  # 스크립트 정확도 (0~100%)
    syllables_per_second = models.FloatField(null=True, blank=True)  # 초당 음절 개수
    speed = models.CharField(max_length=10, null=True, blank=True)  # 'fast' or 'slow'
    um_count = models.IntegerField(default=0)  # '음' 개수
    uh_count = models.IntegerField(default=0)  # '어' 개수
    geu_count = models.IntegerField(default=0)  # '그' 개수

    # 영상 분석 결과
    bad_gesture_count = models.IntegerField(default=0)  # 부적절한 제스처
    good_gesture_count = models.IntegerField(default=0)  # 좋은 제스처
    standing_on_one_leg_count = models.IntegerField(default=0)  # 짝다리 횟수

    # 공통 메타데이터
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Upload {self.upload.id} (Created: {self.created_at})"

    # 점수 종합 계산
    def calculate_overall_score(self):
        nlp_score = (self.accuracy or 0) / 2  # 정확도를 50% 반영
        gesture_score = (self.good_gesture_count - self.bad_gesture_count) * 2
        return max(0, nlp_score + gesture_score)