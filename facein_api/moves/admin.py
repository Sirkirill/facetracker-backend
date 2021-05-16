from django.contrib import admin
from django.contrib.admin import ModelAdmin

from companies.models import Room
from facein_api.admin import admin_site
from facein_api.admin import main_admin_site
from moves.models import Camera


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
