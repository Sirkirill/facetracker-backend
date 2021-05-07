from rest_framework.exceptions import AuthenticationFailed

from facein_api.authentication import RedisAuthentication
from facein_api.usecases import UseCase
from profiles.models import User


class LoginUser(UseCase):
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def execute(self):
        try:
            user = User.objects.get(username=self.username)
        except User.DoesNotExist:
            raise AuthenticationFailed('Username is not found.')

        if user.check_password(self.password):
            token = RedisAuthentication.create_user_session(user.id)
        else:
            raise AuthenticationFailed('User password is wrong.')

        return {'user': user.id, 'token': token}


class LogoutUser(UseCase):
    def __init__(self, request):
        self.request = request

    def execute(self):
        RedisAuthentication.drop_current_session(self.request)
