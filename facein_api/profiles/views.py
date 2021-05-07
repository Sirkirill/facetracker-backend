from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from facein_api.usecases import UseCaseMixin
from profiles.serializers import LoginSerializer
from profiles.serializers import ProfileSerializer
from profiles.usecases import LoginUser
from profiles.usecases import LogoutUser

User = get_user_model()


class LoginView(APIView, UseCaseMixin):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    usecase = LoginUser

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = self._run_usecase(**serializer.validated_data)

        return Response(data)


class LogoutView(APIView, UseCaseMixin):
    permission_classes = [IsAuthenticated]
    usecase = LogoutUser

    def get(self, request):
        self._run_usecase(request=request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
