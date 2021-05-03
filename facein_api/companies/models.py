from django.core.exceptions import ValidationError
from django.db import models


class Company(models.Model):
    """
    Company model. Company is a customer of FaceIn.

    Attributes:
        name (str): Name of the company.
        is_active (bool): Company is using FaceIn currently.

    """
    name = models.CharField(max_length=255,
                            unique=True,
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
