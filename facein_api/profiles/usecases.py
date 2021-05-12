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

        return {'id': user.id, 'username': user.username, 'token': token}


class LogoutUser(UseCase):
    def __init__(self, request):
        self.request = request

    def execute(self):
        RedisAuthentication.drop_current_session(self.request)


class PromoteSecurity(UseCase):
    """Make user a security guide."""
    def __init__(self, user):
        self.user = user

    def execute(self):
        self.user.is_security = True
        self.user.save()


class DemoteSecurity(UseCase):
    """Take the security guard position from the user."""
    def __init__(self, user):
        self.user = user

    def execute(self):
        self.user.is_security = False
        self.user.save()
