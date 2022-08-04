from django.shortcuts import render

# Create your views here.
from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("address", views.AddressViewSet, "address")
router.register("country", views.CountryViewSet, "country")
router.register("province", views.ProvinceViewSet, "province")
router.register("district", views.DistrictViewSet, "district")
router.register("ward", views.WardViewSet, "ward")
router.register("ethnic", views.EthnicViewSet, "ethnic")


urlpatterns = [
    path('', include(router.urls)),
    path('province/list_by_country_id', views.ProvinceViewSet.as_view({
        'get': 'list_by_countryId'
    })),
    path('district/list_by_province_id', views.DistrictViewSet.as_view({
        'get': 'list_by_provinceId'
    })),
    path('ward/list_by_district_id', views.WardViewSet.as_view({
        'get': 'list_by_districtId'
    })),
]
