
from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorUpdateSerializer(serializers.ModelSerializer):
    phone=serializers.CharField(max_length=15)
    country=serializers.CharField(max_length=40)
    province=serializers.CharField(max_length=40)
    district=serializers.CharField(max_length=40)
    ward=serializers.CharField(max_length=40)

    class Meta:
        model = Doctor
        exclude = ['user', 'is_accept']