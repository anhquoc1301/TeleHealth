from django.shortcuts import render

# Create your views here.
from django.urls import path,include

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("", views.DoctorViewSet, "doctor")


urlpatterns = [
    path('', include(router.urls)),
]
