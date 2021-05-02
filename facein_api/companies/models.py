from django.core.exceptions import ValidationError
from django.db import models

from profiles.models import User


class Company(models.Model):
    """
    Company model. Company is a customer of FaceIn.

    Attributes:
        name (str): Name of the company.
        is_active (bool): Company is using FaceIn currently.

    """
    name = models.CharField(max_length=255,
                            default='FaceIn',
                            verbose_name='Компания')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активная',
                                    help_text='Компания пользуется услугами в данный момент')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Room(models.Model):
    """
    Room of the company's office.

    company (Company): Company - owner of the room.
    name (str): Room name.
    info (str): Room description.
    is_whitelisted (bool): if True only restricted group of people is authorized to entrance
        otherwise everyone is authorized except the black list.
    """
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name='rooms',
                                related_query_name='room',
                                verbose_name='Компания')
    name = models.CharField(max_length=255,
                            verbose_name='Помещение')
    info = models.TextField(max_length=1023,
                            blank=True,
                            verbose_name='Описание комнаты')
    is_whitelisted = models.BooleanField(default=False,
                                         verbose_name='Помещение с белым списком',
                                         help_text='В помещение может попасть определенный '
                                                   'круг людей (иначе все, кроме черного списка)')

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'
        unique_together = ('company', 'name')


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
                             verbose_name='Пользователь')
    room = models.ForeignKey(Room,
                             on_delete=models.CASCADE,
                             related_name='user_lists',
                             related_query_name='user_list',
                             verbose_name='Помещение')
    is_blacklisted = models.BooleanField(default=False, verbose_name='В черном списке')
    is_whitelisted = models.BooleanField(default=False, verbose_name='В белом списке')

    class Meta:
        verbose_name = 'Черный и Белый Списки Помещения'
        verbose_name_plural = 'Черный и Белый Списки Помещений'
        unique_together = ['room', 'user']

    def clean(self):
        if self.is_blacklisted and self.is_whitelisted:
            raise ValidationError("User can't be both in black list and white list")
