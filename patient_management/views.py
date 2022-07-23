from doctor.models import Doctor
from patient.serializers import PatientSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.mixins import GetSerializerClassMixin
from .models import  PatientManagement
from .serializers import PatientManagementSerializer
from rest_framework import generics, status, permissions
from apartment.message import error,sucsess

from authentication.models import User
from apartment.pagination import CustomNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from expenses.permissions import Roler3,Roler5, Roler1

class PatientManagementViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = PatientManagement.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PatientManagementSerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        "create": [permissions.IsAuthenticated],
        "retrieve": [Roler1|Roler3],
        "update": [Roler5],
        "destroy": [Roler3],
    }

    @action(
        methods=["GET"],
        detail=False,
        url_path="list_patient"
    )
    def listPatientByDoctorId(self, request):
        doctor = Doctor.objects.get(user=request.user.id)
        patients = PatientManagement.objects.filter(doctor=doctor)
        patientsSerializer=PatientManagementSerializer(patients, many=True)
        return Response(data=patientsSerializer.data, status=status.HTTP_200_OK)