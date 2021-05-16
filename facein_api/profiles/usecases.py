import os

from django.contrib.auth.models import Group
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError

from common.usecases import UseCase
from facein_api.authentication import RedisAuthentication
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


class ChangePassword(UseCase):
    def __init__(self, user, old_password, new_password_1, new_password_2):
        self.user = user

        if not self.user.check_password(old_password):
            raise AuthenticationFailed('Old password is incorrect.')
        if new_password_1 != new_password_2:
            raise ValidationError('Passwords are not the same')  # may be sent to serializer

        self.password = new_password_1

    def execute(self):
        self.user.set_password(self.password)
        self.user.save()


class RegisterUser(UseCase):

    def __init__(self, obj, company_id=None):
        """
        Attributes:
            user: user which is creating a new user.
            company_id: company in which User is created.
        """
        self.obj = obj
        self.company_id = company_id

    def execute(self):
        default_password = os.urandom(32).hex()
        self.obj.set_password(default_password)
        self.obj.info += f'\ndefault password :{default_password}'
        # Here should be checked that obj already has company_id field. Now this is done before.
        if self.company_id:
            self.obj.company_id = self.company_id
        self.obj.save()
        if self.obj.is_admin:
            self.obj.groups.add(Group.objects.get(name='Admin'))
