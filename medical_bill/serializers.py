
from rest_framework import serializers
from .models import MedicalBill


class MedicalBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalBill
        fields = '__all__'