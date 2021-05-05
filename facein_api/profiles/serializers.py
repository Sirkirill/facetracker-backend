from rest_framework import serializers
from rest_framework.serializers import Serializer


class LoginSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

