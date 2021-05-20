# Create your views here.
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.usecases import UseCaseMixin
from companies.models import Company
from companies.serializers import CompanySerializer
from moves.serializers import MoveInput
from moves.usecases import GetCompanyCameras
from moves.usecases import MakePhotoObjectFromPhoto
from profiles.usecases import UserPassCamera


class GetCameras(APIView, UseCaseMixin):
    usecase = GetCompanyCameras
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        result = {}
        for company in Company.objects.all():
            companies = self._run_usecase(company.id)
            result[company.id] = companies
        return Response(result)


class GetCompaniesView(APIView, UseCaseMixin):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        companies = Company.objects.filter(is_active=True)
        return Response(CompanySerializer(companies, many=True).data)


class MoveView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = MoveInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        camera = serializer.validated_data['camera']
        photo = serializer.validated_data['photo']
        photo = MakePhotoObjectFromPhoto(photo, company_id=camera.to_room.company_id).execute()
        UserPassCamera(camera=camera, photo=photo, user=photo.user).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)
