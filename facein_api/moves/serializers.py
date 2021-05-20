from rest_framework import serializers

from moves.models import Camera


class MoveInput(serializers.Serializer):
    camera = serializers.PrimaryKeyRelatedField(queryset=Camera.objects.all())
    photo = serializers.ImageField()
