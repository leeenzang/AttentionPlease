from django.db import models
from django.conf import settings

class UserUpload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='uploads/')
    script = models.TextField()  # 사용자 제공 스크립트
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 업로드 시간
    processed_audio = models.FileField(upload_to='processed_audio/', null=True, blank=True)  # NLP팀용 오디오 파일
    processed_video = models.FileField(upload_to='processed_video/', null=True, blank=True)  # 영상팀용 비디오 파일
    processed_at = models.DateTimeField(null=True, blank=True)  # 처리 완료 시간
    
    def __str__(self):
        return f"Upload by {self.user.username} on {self.uploaded_at}"