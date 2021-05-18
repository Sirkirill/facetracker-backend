from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from facein_api.admin import admin_site
from facein_api.admin import main_admin_site
from photos.models import Photo


@admin.register(Photo, site=main_admin_site)
class ImageAdmin(ModelAdmin):
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


@admin.register(Photo, site=admin_site)
class ImageAdmin(ModelAdmin):
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
