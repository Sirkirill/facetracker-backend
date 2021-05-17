from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import Action
from common.permissions import IsAdmin
from common.permissions import IsSuperUser
from common.usecases import UseCaseMixin
from companies.models import Room
from profiles.serializers import ChangePasswordSerializer
from profiles.serializers import LoginSerializer
from profiles.serializers import ProfileSerializer
from profiles.serializers import StaffSerializer
from profiles.usecases import ChangePassword
from profiles.usecases import CheckAbilityToEnterRoom
from profiles.usecases import LoginUser
from profiles.usecases import LogoutUser

User = get_user_model()


class LoginView(APIView, UseCaseMixin):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    usecase = LoginUser

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = self._run_usecase(**serializer.validated_data)

        return Response(data)


class ChangePasswordView(APIView, UseCaseMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    usecase = ChangePassword

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        self._run_usecase(request.user, **serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class LogoutView(APIView, UseCaseMixin):
    usecase = LogoutUser

    def get(self, request):
        self._run_usecase(request=request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(APIView):
    """
    API for getting and updating user's profile.
    """
    serializer_class = ProfileSerializer

    def get(self, request):
        return Response(self.serializer_class(request.user).data)

    @swagger_auto_schema(request_body=ProfileSerializer)
    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.serializer_class(request.user).data)


class StaffViewSet(viewsets.ModelViewSet):
    """
    API for staff managing.

    list: Get list of all profiles. Details in list method.
        Is available for everyone who is authenticated.
    retrieve: Get user data. Is available for everyone who is authenticated.
    create: Create new user. Only admins of company and superusers can create new users.
    delete: Delete user. Only admins of company and superusers can delete users.
    update: Update user. Only admins of company and superusers can update users.

    """
    queryset = User.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsSuperUser
                          | (Action.retrieve | Action.list) & IsAuthenticated
                          | (Action.create | Action.update | Action.delete) & IsAdmin]

    def update(self, request, *args, **kwargs):
        """"Update user. Update is always partial."""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def list(self, request):
        """
        List of all users.
        Superuser receives all the users.
        Admin receives all the users of the admin company.
        Security receives all the users of the securities company.
        Ordinary user receives only active users in user company.
        """
        users_filter = Q()
        if not request.user.is_superuser:
            users_filter &= Q(company_id=request.user.company.id)
        if not request.user.is_admin and not request.user.is_securitys:
            users_filter &= Q(is_blacklisted=True)
        queryset = User.objects.filter(users_filter)
        return Response(data=self.serializer_class(queryset, many=True).data)


class CheckAbilityToEnterRoomView(APIView, UseCaseMixin):
    usecase = CheckAbilityToEnterRoom

    def get(self, request, user_id, room_id):
        room = get_object_or_404(Room, pk=room_id)
        user = get_object_or_404(User, pk=user_id)
        permission, errors = self._run_usecase(user, room)
        if permission:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_202_ACCEPTED, data=errors)
