from django.core.management.commands.runserver import Command as runserver
from photos.management.commands.load_images import Command as load_images


class Command(runserver):
    def handle(self, *args, **options):
        load_images().handle()
        super().handle(*args, **options)
