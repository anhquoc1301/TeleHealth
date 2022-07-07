from django.shortcuts import render

# Create your views here.
from django.urls import path,include

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("patient_management", views.PatientManagementViewSet, "patient_management")


urlpatterns = [
    path('', include(router.urls)),
]
