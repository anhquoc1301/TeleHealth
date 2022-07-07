from django.shortcuts import render

# Create your views here.
from django.urls import path,include

from .views import CompanyViewset

from rest_framework import routers
from . import views
from .views import CompanyViewset

router = routers.DefaultRouter()
router.register("company", views.CompanyViewset, "company")


urlpatterns = [
    path('', include(router.urls)),
    # path('company/company/<int:id>', CompanyViewset.as_view({
    #     'get': 'detail_company'

]
