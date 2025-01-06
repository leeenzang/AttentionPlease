from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)  # 요청 데이터 받기
        if serializer.is_valid():  # 데이터 검증
            serializer.save()  # 유저 생성
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 에러 반환
    

class LoginView(TokenObtainPairView):
    pass

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]  # 클라이언트에서 받은 refresh 토큰
            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트에 등록
            return Response({'message': 'Logout successful!'}, status=200)
        except Exception as e:
            return Response({'error': 'Something went wrong'}, status=400)