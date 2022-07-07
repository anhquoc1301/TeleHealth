from django.shortcuts import render

# Create your views here.
from django.urls import path,include

from .views import CompanyViewset, ProposalViewSet

from rest_framework import routers
from . import views
from .views import CompanyViewset

router = routers.DefaultRouter()
router.register("doctor", views.CompanyViewset, "doctor")
router.register("patient", views.ProposalViewSet, "patient")
router.register("medical_unit", views.ProposalViewSet, "medical_unit")
router.register("medical_bill", views.ProposalViewSet, "medical_bill")
router.register("address", views.ProposalViewSet, "address")



urlpatterns = [
    path('', include(router.urls)),
    # path('company/company/<int:id>', CompanyViewset.as_view({
    #     'get': 'detail_company'

]
