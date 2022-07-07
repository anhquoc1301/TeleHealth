
from rest_framework import serializers
from .models import MedicalUnit


class MedicalUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalUnit
        fields = '__all__'
