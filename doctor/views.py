from django.shortcuts import get_object_or_404
from address.models import Address
from authentication.permissions import Role1, Role2, Role3, Role4
from authentication.serializer import RegisterSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.mixins import GetSerializerClassMixin
from .models import Doctor
from .serializers import DoctorSerializer, DoctorUpdateSerializer
from rest_framework import generics, status, permissions
from base.message import success, error

from authentication.models import User
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action


class DoctorViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Doctor.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorSerializer
    serializer_action_classes = {
        "update_profile_doctor": DoctorUpdateSerializer,
    }
    permission_classes_by_action = {
        'list': [AllowAny],
        "update_profile_doctor": [Role1],
        "destroy": [Role4],
    }

    @action(
        methods=["POST"],
        detail=False,
        url_path="update_profile_doctor"
    )
    def update_profile_doctor(self, request):
        try:
            user_id = request.user.id
            if user_id:
                doctor = get_object_or_404(Doctor, user_id=user_id)
                address = Address.objects.create(
                    country_id=request.data['country'], 
                    province_id=request.data['province'], 
                    district_id=request.data['district'], 
                    ward_id=request.data['ward']
                    )
                request.data['address']=address.id
                doctorSerializer = self.get_serializer(
                    instance=doctor, data=request.data, partial=True)
                doctorSerializer.is_valid(raise_exception=True)
                self.perform_update(doctorSerializer)
                user = User.objects.get(id=user_id)
                user.phone = request.data['phone']
                user.save()
                return success(data=doctorSerializer.data)
            else:
                raise Exception('not valid')
        except(Exception):
            return error(data=Exception)
