from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from companies.serializers import RoomSerializer
from photos.models import Photo
from photos.models import Post


class PhotoSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        if not obj:
            return None
        return f'{obj.username}:{obj.first_name} {obj.last_name}'

    class Meta:
        model = Photo
        fields = ('image', 'user')


class PostSerializer(ModelSerializer):
    room = RoomSerializer()
    photo = PhotoSerializer()
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        return obj.move.date

    def to_representation(self, instance):
        instance.room = instance.move.camera.to_room
        return super().to_representation(instance)

    class Meta:
        model = Post
        fields = ('pk', 'room', 'photo', 'is_important', 'is_reacted', 'note', 'date')
