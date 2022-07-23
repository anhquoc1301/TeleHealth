from authentication.serializer import RegisrerSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.mixins import GetSerializerClassMixin
from .models import  MedicalUnit
from .serializers import  MedicalUnitSerializer
from rest_framework import generics, status, permissions
from apartment.message import error,sucsess

from authentication.models import User
from apartment.pagination import CustomNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from expenses.permissions import Roler3,Roler5, Roler1


class MedicalUnitViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = MedicalUnit.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MedicalUnitSerializer
    
    
    def create(self, request):
        userData = request.data['user']
        medicalData = request.data['medical']
        userSerializer = RegisrerSerializer(data=userData)
        if userSerializer.is_valid():
            newUser=User.objects.create_user(email=userData['email'], password=userData['password'], username=userData['username'], phone=userData['phone'], roler=userData['roler'])
            medicalData['user']=newUser.id
            medicalSerializer = self.get_serializer(data=medicalData)
            if medicalSerializer.is_valid():
                medicalSerializer.save()
                return sucsess(data=medicalSerializer.data)
        return error()

    @action(
        methods=["POST"],
        detail=False,
        url_path="add_patient"
    )
    def addPatient(self, request):
        userData = request.data['user']
        patientData = request.data['patient']
        userSerializer = RegisrerSerializer(data=userData)
        if userSerializer.is_valid():
            newUser=User.objects.create_user(email=userData['email'], password=userData['password'], username=userData['username'], phone=userData['phone'], roler=userData['roler'])
            patientData['user']=newUser.id
            patientSerializer = self.get_serializer(data=patientData)
            if patientSerializer.is_valid():
                patientSerializer.save()
                return sucsess(data=patientSerializer.data)
        return error()