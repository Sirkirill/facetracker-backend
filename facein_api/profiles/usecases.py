import os

from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError

from common.usecases import UseCase
from facein_api.authentication import RedisAuthentication
from moves.models import MoveLog
from photos.models import Post
from profiles.models import BlackWhiteList
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

        return {'id': user.id, 'username': user.username, 'token': token,
                'is_security': user.is_security}


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

    def __init__(self, user, company_id=None):
        """
        Attributes:
            user: user which is creating a new user.
            company_id: company in which User is created.
        """
        self.user = user
        self.company_id = company_id

    def execute(self):
        default_password = os.urandom(32).hex()
        self.user.set_password(default_password)
        self.user.info += f'\ndefault password :{default_password}'
        # Here should be checked that obj already has company_id field. Now this is done before.
        if self.company_id:
            self.user.company_id = self.company_id
        self.user.save()
        if self.user.is_admin:
            self.user.groups.add(Group.objects.get(name='Admin'))


class CheckAbilityToEnterRoom(UseCase):

    def __init__(self, user, room):
        """
        Attributes:
            user: user which is creating a new user.
            room: room to which User is trying to enter.
        """
        self.user = user
        self.room = room

    def execute(self):
        errors = []
        if self.user:
            if self.user.is_blacklisted:
                errors.append(_("User is blacklisted for this company"))
            if self.room.company != self.user.company:
                errors.append(_("User is from another company."))
            try:
                list_record = BlackWhiteList.objects.get(user=self.user, room=self.room)
                if self.room.is_whitelisted and not list_record.is_whitelisted:
                    errors.append(_("User is not from the whitelist of the whitelisted room"))
                if list_record.is_blacklisted:
                    errors.append(_('User is blacklisted for this room'))
            except BlackWhiteList.DoesNotExist:
                if self.room.is_whitelisted:
                    errors.append(_("User is not from the whitelist of the whitelisted room"))
        if not self.user:
            if self.room.is_whitelisted:
                errors.append(_("User is not from the whitelist of the whitelisted room"))
        if errors:
            return False, '; '.join([str(error) for error in errors])
        return True, None


class CheckAbilityToPassCamera(UseCase):
    def __init__(self, user, camera):
        self.user = user
        self.camera = camera

    def execute(self):
        return CheckAbilityToEnterRoom(self.user, self.camera.to_room).execute()


class UserPassCamera(UseCase):
    def __init__(self, camera, user=None, photo=None):
        self.camera = camera
        self.user = user
        self.photo = photo

    def execute(self):
        permission, errors = CheckAbilityToPassCamera(self.user, self.camera).execute()
        move = MoveLog.objects.create(camera=self.camera, user=self.user)
        if not permission:
            Post.objects.create(move=move, photo=self.photo, note=errors)
