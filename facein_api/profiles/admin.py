from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from companies.models import Room
from facein_api.admin import admin_site
from facein_api.admin import main_admin_site
from .models import BlackWhiteList
from .models import User
from .usecases import RegisterUser


@admin.register(User, site=main_admin_site)
class UserAdmin(ModelAdmin):
    list_filter = ('company', 'is_blacklisted', 'is_admin', 'is_superuser')
    list_display = ('username', 'company', 'is_superuser', 'is_security', 'is_blacklisted')
    fieldsets = (
        (_('Names'), {
            'fields': ('username', ('first_name', 'last_name'))
        }),
        (_('Flags'), {
            'fields': ('is_security', 'is_admin', 'is_blacklisted')
        }),
        (None, {
            'fields': ('company', 'is_superuser', 'info', 'date_joined', 'last_login')
        }),
    )
    readonly_fields = ('date_joined', 'last_login')

    def save_model(self, request, obj, form, change):
        if not change:
            RegisterUser(obj).execute()


@admin.register(User, site=admin_site)
class UserAdmin(ModelAdmin):
    def get_queryset(self, request):
        return User.objects.filter(company_id=request.user.company_id)

    list_filter = ('is_blacklisted', 'is_admin', 'is_security')
    list_display = ('username', 'company', 'is_admin', 'is_security', 'is_blacklisted')
    fieldsets = (
        (_('Names'), {
            'fields': ('username', ('first_name', 'last_name'))
        }),
        (_('Flags'), {
            'fields': ('is_security', 'is_admin', 'is_blacklisted')
        }),
        (None, {
            'fields': ('company', 'info', 'date_joined', 'last_login')
        }),
    )
    readonly_fields = ('company', 'date_joined', 'last_login')

    def save_model(self, request, obj, form, change):
        if not change:
            RegisterUser(obj, request.user.company_id).execute()
        super().save_model(request, obj, form, change)


@admin.register(Group, site=main_admin_site)
class GroupAdmin(ModelAdmin):
    pass


@admin.register(BlackWhiteList, site=main_admin_site)
class BWListAdmin(ModelAdmin):
    list_filter = ('room__is_whitelisted', 'room__company')
    list_display = ('room', 'whitelisted_room', 'user', 'is_blacklisted', 'is_whitelisted')

    def whitelisted_room(self, obj):
        return bool(obj.room.is_whitelisted)

    whitelisted_room.boolean = True
    whitelisted_room.short_description = _('Whitelist room')


@admin.register(BlackWhiteList, site=admin_site)
class BWListAdmin(ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(room__company_id=request.user.company_id)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['room'].queryset = Room.objects.filter(
            company_id=request.user.company_id)
        form.base_fields['user'].queryset = User.objects.filter(
            company_id=request.user.company_id)
        return form

    list_filter = ('room__is_whitelisted', 'room__company')
    list_display = ('room', 'whitelisted_room', 'user', 'is_blacklisted', 'is_whitelisted')

    def whitelisted_room(self, obj):
        return bool(obj.room.is_whitelisted)

    whitelisted_room.boolean = True
    whitelisted_room.short_description = _('Whitelist room')
