# Create your views here.
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from common.usecases import UseCaseMixin
from companies.models import Company
from companies.serializers import CompanySerializer
from moves.usecases import GetCompanyCameras


class GetCameras(APIView, UseCaseMixin):
    usecase = GetCompanyCameras
    permission_classes = [permissions.AllowAny]

    def get(self, request, company_id, *args, **kwargs):
        companies = self._run_usecase(company_id)
        return Response(companies)


class GetCompaniesView(APIView, UseCaseMixin):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        companies = Company.objects.filter(is_active=True)
        return Response(CompanySerializer(companies, many=True).data)
