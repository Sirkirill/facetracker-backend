from django.core.management import BaseCommand

from photos.models import Photo


class Command(BaseCommand):
    help = 'Load images from database to the storage'

    def handle(self, *args, **options):
        for obj in Photo.objects.all():
            obj.load_image()
