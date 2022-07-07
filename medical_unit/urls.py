from django.shortcuts import render

# Create your views here.
from django.urls import path,include

from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register("medical_unit", views.MedicalUnitViewSet, "medical_unit")


urlpatterns = [
    path('', include(router.urls)),
]
