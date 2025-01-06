from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password'] # 클라이언트가 보낼/받을 데이터
        extra_kwargs = {'password': {'write_only': True}} # 비번은 write_only로 설정

    # 클라이언트가 보낸 데이터 받아 새 유저 생성
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user