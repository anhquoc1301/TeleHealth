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