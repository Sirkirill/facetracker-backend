from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from facein_api.admin import admin_site
from facein_api.admin import main_admin_site
from moves.models import MoveLog
from photos.models import Photo
from photos.models import Post
from photos.models import User


@admin.register(Photo, site=main_admin_site)
class ImageAdmin(ModelAdmin):
    search_fields = ('user__username',)
    list_filter = ('user__company',)
    readonly_fields = ['img_preview']
    list_display = ('company', 'user', 'img_short_preview')

    fields = ('image', 'user')

    def company(self, obj):
        if not obj.user:
            return None
        return obj.user.company.name

    def get_queryset(self, request):
        return Photo.objects.select_related('user', 'user__company')

    def img_preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'
                         .format(url=obj.image.url,
                                 width=obj.image.width,
                                 height=obj.image.height)
                         )

    def img_short_preview(self, obj):
        w, h = obj.image.width, obj.image.height
        WIDTH = 200
        return mark_safe('<img src="{url}" width="{width}" height={height} />'
                         .format(url=obj.image.url,
                                 height=WIDTH * h / w,
                                 width=WIDTH)
                         )

    img_preview.short_description = _('Photo preview')
    img_short_preview.short_description = _('Photo preview')


@admin.register(Photo, site=admin_site)
class ImageAdmin(ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].queryset = User.objects.filter(
            company_id=request.user.company_id)
        return form

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user__company_id=request.user.company_id)

    search_fields = ('user__username',)
    readonly_fields = ['img_preview']
    list_display = ('user', 'img_short_preview')

    def img_preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'
                         .format(url=obj.image.url,
                                 width=obj.image.width,
                                 height=obj.image.height)
                         )

    def img_short_preview(self, obj):
        w, h = obj.image.width, obj.image.height
        WIDTH = 200
        return mark_safe('<img src="{url}" width="{width}" height={height} />'
                         .format(url=obj.image.url,
                                 height=WIDTH * h / w,
                                 width=WIDTH)
                         )

    img_preview.short_description = _('Photo preview')
    img_short_preview.short_description = _('Photo preview')


@admin.register(Post, site=main_admin_site)
class PostAdmin(ModelAdmin):
    def date(self, obj):
        return obj.move.date
    date.short_description = _('Event Date')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('photo', 'move', 'move__camera',
                                                            'move__camera__to_room',
                                                            'move__camera__to_room__company')\
            .order_by('-move__date')
    list_filter = ('move__camera__to_room__company__name', 'is_important', 'is_reacted')

    list_display = ('move', 'is_important', 'is_reacted', 'date')


@admin.register(Post, site=admin_site)
class PostAdmin(ModelAdmin):
    def date(self, obj):
        return obj.move.date
    date.short_description = _('Event Date')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['move'].queryset = MoveLog.objects.filter(
            camera__to_room__company_id=request.user.company_id)
        return form

    def get_queryset(self, request):
        return super().get_queryset(request)\
            .filter(move__camera__to_room__company_id=request.user.company_id)\
            .select_related('photo', 'move', 'move__camera', 'move__camera__to_room',
                            'move__camera__to_room__company').order_by('-move__ date')

    list_filter = ('is_important', 'is_reacted')
    list_display = ('move', 'is_important', 'is_reacted', 'date')
