from rest_framework import serializers
from rest_framework.serializers import Serializer

from profiles.models import User


class LoginSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    """User serializer for manipulations made by user."""
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = User
        fields = ('pk',
                  'username',
                  'first_name', 'last_name',
                  'company',
                  'is_superuser', 'is_security', 'is_admin', 'is_blacklisted',
                  'date_joined', 'last_login')
        read_only_fields = ('pk',
                            'is_superuser', 'is_security', 'is_admin', 'is_blacklisted',
                            'date_joined', 'last_login')


class StaffSerializer(serializers.ModelSerializer):
    """User serializer for manipulations made by user admin."""
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = User
        fields = ('pk',
                  'username',
                  'first_name', 'last_name',
                  'company',
                  'is_superuser', 'is_security', 'is_admin', 'is_blacklisted',
                  'date_joined', 'last_login')
        read_only_fields = ('pk',
                            'is_superuser',
                            'date_joined', 'last_login')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password_1 = serializers.CharField(required=True)
    new_password_2 = serializers.CharField(required=True)


class StaffSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
