from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from PIL import Image

from moves.models import MoveLog

User = get_user_model()


class Photo(models.Model):
    """
    Image. Is stored as binary in database. To make it working using Heroku all photos are loaded
        from database before script running using management command load_images.

    Attributes:
        image: ImageField. Uses image from media folder.
        image_binary: Image in database stored as binary.
        user: User who is pictured on photo. May be null is user is not specified.

    """
    image = models.ImageField(_('Photo'), null=True)
    image_binary = models.BinaryField(null=True, editable=False)
    user = models.ForeignKey(User, null=True, blank=True, related_name='photos',
                             on_delete=models.SET_NULL, verbose_name=_('User'))

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def clean(self):
        if not all([letter.isalnum() or letter in ['_', '.'] for letter in self.image.name]):
            raise ValidationError(_('Image name should contain only alphanumeric characters or _'))

    def __str__(self):
        if self.image:
            return self.image.name
        return f'Photo {self.pk}'

    def save(self, *args, **kwargs):
        with BytesIO() as output:
            with Image.open(self.image) as img:
                img.save(output, img.format)
            self.image_binary = output.getvalue()
        super().save(*args, **kwargs)

    def load_image(self):
        if self.image and self.image_binary:
            try:
                self.image.open()
            except FileNotFoundError:
                Image.open(BytesIO(self.image_binary)).save(self.image.path)


class Post(models.Model):
    """
    Post which is created for sending to securities information about users which are trying
        to move to the rooms they are not allowed.
    """
    move = models.OneToOneField(MoveLog, null=True, related_name='post', on_delete=models.SET_NULL,
                                verbose_name=_('MoveLog'))
    photo = models.ForeignKey(Photo, verbose_name=_('Photo'),
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              null=True, blank=True)
    is_important = models.BooleanField(_("Post is important"), default=False)
    is_reacted = models.BooleanField(_('Somebody has already reacted on the post'), default=False)
    note = models.TextField(_('Additional notes'), max_length=255, blank=True)

    def __str__(self):
        return str(self.move)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
