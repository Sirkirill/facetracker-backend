from django.contrib import admin
from django.contrib.admin import ModelAdmin

from companies.models import Company
from companies.models import Room
from facein_api.admin import admin_site
from facein_api.admin import main_admin_site


@admin.register(Company, site=main_admin_site)
class CompanyAdmin(ModelAdmin):
    list_display = ('name', 'is_active')
    ordering = ['-is_active']


@admin.register(Room, site=main_admin_site)
class RoomAdmin(ModelAdmin):
    list_filter = ('company', 'is_whitelisted',)
    list_display = ('name', 'company', 'is_whitelisted')


@admin.register(Room, site=admin_site)
class RoomAdmin(ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(company_id=request.user.company_id)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['company'].queryset = Company.objects.filter(id=request.user.company_id)
        return form

    list_filter = ('is_whitelisted', )
    list_display = ('name', 'company', 'is_whitelisted')
    fields = ('name', 'company', 'is_whitelisted', 'info')
