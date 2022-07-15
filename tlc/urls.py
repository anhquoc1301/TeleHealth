from os import name
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('load_file/',LoadFile.as_view(), name='load_file'),
]
