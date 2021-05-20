from rest_framework.serializers import ModelSerializer

from companies.serializers import RoomSerializer
from photos.models import Photo
from photos.models import Post
from profiles.serializers import StaffSerializer


class PhotoSerializer(ModelSerializer):
    user = StaffSerializer()

    class Meta:
        model = Photo
        fields = ('image', 'user')


class PostSerializer(ModelSerializer):
    room = RoomSerializer()
    photo = PhotoSerializer()

    def to_representation(self, instance):
        instance.room = instance.move.camera.to_room
        return super().to_representation(instance)

    class Meta:
        model = Post
        fields = ('pk', 'room', 'photo', 'is_important', 'is_reacted', 'note')
