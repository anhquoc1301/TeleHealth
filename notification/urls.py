from django.shortcuts import render

# Create your views here.
from django.urls import path,include

from rest_framework import routers
from . import views
from .views import CompanyViewset

router = routers.DefaultRouter()
router.register("notification", views.CompanyViewset, "company")


urlpatterns = [
    path('', include(router.urls)),
    # path('company/company/<int:id>', CompanyViewset.as_view({
    #     'get': 'detail_company'

]
