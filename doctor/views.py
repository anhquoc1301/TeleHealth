from authentication.serializer import RegisrerSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.mixins import GetSerializerClassMixin
from .models import Doctor
from .serializers import  DoctorSerializer
from rest_framework import generics, status, permissions
from apartment.message import error,sucsess

from authentication.models import User
from apartment.pagination import CustomNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from expenses.permissions import Roler3,Roler5, Roler1


class DoctorViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Doctor.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = DoctorSerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        # "create": [permissions.IsAuthenticated],
        "retrieve": [Roler1|Roler3],
        "update": [Roler5],
        "destroy": [Roler3],
    }

    def create(self, request):
        userData = request.data['user']
        doctorData = request.data['doctor']
        userSerializer = RegisrerSerializer(data=userData)
        if userSerializer.is_valid():
            newUser=User.objects.create_user(email=userData['email'], password=userData['password'], username=userData['username'], phone=userData['phone'], roler=userData['roler'])
            doctorData['user']=newUser.id
            doctorSerializer = self.get_serializer(data=doctorData)
            if doctorSerializer.is_valid():
                doctorSerializer.save()
                return sucsess(data=doctorSerializer.data)
        return error()

