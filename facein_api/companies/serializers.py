from rest_framework import serializers

from companies.models import Company
from companies.models import Room


class RoomSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Room
        fields = ('company', 'name', 'info', 'is_whitelisted')


class CompanySerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('pk', 'name', 'is_active', 'rooms')
