from os import name
from django.contrib import admin
from django.urls import path
from .views import PcApi


urlpatterns = [
    path('pc_result', PcApi.as_view(), name = 'pc_api')
]
