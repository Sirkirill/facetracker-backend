from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from companies.models import Company
from companies.models import Room


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_security', False)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_blacklisted', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        company = Company.objects.get(name='FaceIn')
        extra_fields.setdefault('company', company)

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model. User can exist only in one company otherwise user has to have several profiles.

    Attributes:
        username (str): Unique username. Is used in auth system.
        first_name (str): User's first name.
        last_name (str): User's last name.
        is_security (bool): True if User is a security guard and has a mobile app False otherwise.
        is_admin (bool): True if User is an admin of the customer company.
        is_blacklisted (bool): True if User is in Company black list.
        info (str): User description.
        date_joined (datetime): Date and time when user profile was created.

    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_security = models.BooleanField(
        _('security status'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as '
            'security guard of the customer company. '
        ),
    )
    is_admin = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_(
            _('Designates whether this user should be treated as admin of the customer company. ')
        ),
    )
    is_blacklisted = models.BooleanField(
        _('blacklisted'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
        ),
    )

    info = models.TextField(
        _('Additional notes'),
        max_length=255,
        blank=True
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                verbose_name=_('Company'),
                                related_name='users',
                                related_query_name='user')

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['username']
        constraints = [
            models.CheckConstraint(check=~models.Q(is_superuser=True, is_blacklisted=True),
                                   name='superusers_are_not_blocked')
        ]

    def __str__(self):
        return self.username

    def clean(self):
        if self.is_superuser and self.is_blacklisted:
            raise ValidationError(_("Superuser can't be blocked"))
        company = Company.objects.get(name='FaceIn')
        if self.is_superuser and self.company_id != company.id:
            raise ValidationError("Superuser should be a member of FaceIn company")

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    @property
    def is_staff(self):
        return self.is_superuser or self.is_admin


class BlackWhiteList(models.Model):
    """
    Relation between User and Room. Stores room's white or black list of users.
    Black list is list of users which can't come to the room.
    White list is list of users which only can come to the room.

    Attributes:
        user (User): Company User.
        room (Room): Company room.
        is_blacklisted (bool): True if user is in room black list.
        is_whitelisted (bool): True if user is in room white list.

    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='rooms',
                             related_query_name='room',
                             verbose_name=_('User'))
    room = models.ForeignKey(Room,
                             on_delete=models.CASCADE,
                             related_name='user_lists',
                             related_query_name='user_list',
                             verbose_name=_('Room'))
    is_blacklisted = models.BooleanField(default=False, verbose_name=_('Blacklisted'))
    is_whitelisted = models.BooleanField(default=False, verbose_name=_('Whitelisted'))

    class Meta:
        verbose_name = _('Black list and white list')
        verbose_name_plural = _('Black lists and white lists')
        unique_together = ['room', 'user']

    def clean(self):
        if self.is_blacklisted and self.is_whitelisted:
            raise ValidationError("User can't be both in black list and white list")
