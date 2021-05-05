from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from facein_api.authentication import RedisAuthentication
from profiles.serializers import LoginSerializer

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('Username is not found.')

        if user.check_password(password):
            token = RedisAuthentication.create_user_session(user.id)
        else:
            raise AuthenticationFailed('User password is wrong.')

        return Response(data={'user': user.id, 'token': token})
