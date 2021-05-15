import os

from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import ugettext_lazy as _

from facein_api.admin import main_admin_site
from .models import User


@admin.register(User, site=main_admin_site)
class UserAdmin(ModelAdmin):
    start_password = forms.CharField()

    list_display = ('username', 'company', 'is_superuser', 'is_security', 'is_blacklisted')
    fieldsets = (
        (_('Names'), {
            'fields': ('username', ('first_name', 'last_name'))
        }),
        (_('Flags'), {
            'fields': ('is_security', 'is_admin', 'is_blacklisted')
        }),
        (None, {
            'fields': ('company', 'is_superuser', 'info', )
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            default_password = os.urandom(32).hex()
            obj.set_password(default_password)
            obj.info = obj.info + f'\ndefault password :{default_password}\n'
        return super().save_model(request, obj, form, change)
