from django.contrib import admin
from django.contrib.admin import ModelAdmin

from companies.models import Company
from companies.models import Room
from facein_api.admin import main_admin_site


@admin.register(Company, site=main_admin_site)
class CompanyAdmin(ModelAdmin):
    list_display = ('name', 'is_active')
    ordering = ['-is_active']


@admin.register(Room, site=main_admin_site)
class RoomAdmin(ModelAdmin):
    list_display = ('company', 'name', 'is_whitelisted')
