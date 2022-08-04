from authentication.permissions import Role2, Role1, Role3, Role4
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.mixins import GetSerializerClassMixin
from .models import Address, Country, District, Ethnic, Province, Ward
from .serializers import AddressSerializer, CountrySerializer, DistrictSerializer, EthnicSerializer, ProvinceSerializer, WardSerializer
from rest_framework import generics, status, permissions
from base.message import success, error
from authentication.models import User
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action


class AddressViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        "create": [permissions.IsAuthenticated],
    }
class CountryViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Country.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CountrySerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        "create": [Role3],
    }
class ProvinceViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Province.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProvinceSerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        'create': [Role3],
        'list_by_countryId': [AllowAny],
    }

    # @action(
    #     methods=["GET"],
    #     detail=False,
    #     url_path="list_by_country_id"
    # )
    def list_by_countryId(self, request, *args, **kwargs):
        countryId = self.request.GET.get('pk')
        print(countryId)
        provinces=Province.objects.filter(country_id=countryId)
        provincesSerializer=ProvinceSerializer(provinces, many=True)
        return success(data=provincesSerializer.data)

class DistrictViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = District.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DistrictSerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        "create": [Role3],
        'list_by_provinceId': [AllowAny],
    }

    def list_by_provinceId(self, request, *args, **kwargs):
        provinceId = self.request.GET.get('pk')
        districts=District.objects.filter(province_id=provinceId)
        districtsSerializer=DistrictSerializer(districts, many=True)
        return success(data=districtsSerializer.data)
class WardViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Ward.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = WardSerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        "create": [Role3],
        'list_by_districtId': [AllowAny],

    }

    def list_by_districtId(self, request, *args, **kwargs):
        districtId = self.request.GET.get('pk')
        wards=Ward.objects.filter(country_id=districtId)
        wardsSerializer=WardSerializer(wards, many=True)
        return success(data=wardsSerializer.data)
class EthnicViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Ethnic.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EthnicSerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        "create": [Role3],
    }