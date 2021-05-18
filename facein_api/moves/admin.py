from django.contrib import admin
from django.contrib.admin import ModelAdmin

from companies.models import Room
from facein_api.admin import admin_site
from facein_api.admin import main_admin_site
from moves.models import Camera
from moves.models import MoveLog
from profiles.models import User


@admin.register(Camera, site=main_admin_site)
class CameraAdmin(ModelAdmin):
    list_filter = ('from_room__company',)
    list_display = ('company', 'camera',)

    def company(self, obj):
        return obj.from_room.company

    def camera(self, obj):
        return f'{obj.from_room}->{obj.to_room}'


@admin.register(Camera, site=admin_site)
class CameraAdmin(ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(from_room__company_id=request.user.company_id)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['from_room'].queryset = Room.objects.filter(
            company_id=request.user.company_id)
        form.base_fields['to_room'].queryset = Room.objects.filter(
            company_id=request.user.company_id)
        return form

    list_display = ('company', 'camera',)

    def company(self, obj):
        return obj.from_room.company

    def camera(self, obj):
        return f'{obj.from_room}->{obj.to_room}'


@admin.register(MoveLog, site=main_admin_site)
class MoveAdmin(ModelAdmin):
    list_filter = ('camera__to_room__company',)
    list_display = ('camera', 'user', 'date')
    search_fields = ('user__username',)


@admin.register(MoveLog, site=admin_site)
class MoveAdmin(ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].queryset = User.objects.filter(
            company_id=request.user.company_id)
        form.base_fields['camera'].queryset = Camera.objects.filter(
            to_room__company_id=request.user.company_id)
        return form

    def get_queryset(self, request):
        return super().get_queryset(request)\
            .filter(camera__to_room__company_id=request.user.company_id)

    list_display = ('camera', 'user', 'date')
    search_fields = ('user__username',)
