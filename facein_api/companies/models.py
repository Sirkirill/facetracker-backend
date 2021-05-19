from django.db import models
from django.utils.translation import ugettext_lazy as _


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
                            verbose_name=_('Company name'))
    is_active = models.BooleanField(default=True,
                                    verbose_name=_('Active'),
                                    help_text=_('Company is using FaceIn now'))

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return self.name


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
                                verbose_name=_('Company'))
    name = models.CharField(max_length=255,
                            verbose_name=_('Room name'))
    info = models.TextField(max_length=1023,
                            blank=True,
                            verbose_name=_('Additional notes'))
    is_whitelisted = models.BooleanField(default=False,
                                         verbose_name=_('Whitelist room'),
                                         help_text=_('Only whitelist of people is allowed '
                                                     'to enter the room, '
                                                     'everybody except blacklist otherwise'))

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        unique_together = ('company', 'name')

    def __str__(self):
        return f'{self.company}:{self.name}'
