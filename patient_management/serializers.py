
from rest_framework import serializers
from .models import PatientManagement



class PatientManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientManagement
        fields = '__all__'