
from authentication.models import User
from rest_framework import serializers
from .models import Patient
from patient_management.models import PatientManagement
from address.models import Address
from address.serializers import AddressSerializer


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            user = User.objects.get(id=instance.user.id)
            patientEmail = user.email
            patientPhone = user.phone
            if PatientManagement.objects.filter(patient_id=instance.id):
                patientManagement = True
            else:
                patientManagement = False
            address = Address.objects.get(id=instance.address.id)
            patientAddress = AddressSerializer(instance=address).data
        except:
            patientEmail = ''
            patientPhone = ''
            patientAddress = ''

        representation['email'] = patientEmail
        representation['phone'] = patientPhone
        representation['address'] = patientAddress
        representation['patientManagement'] = patientManagement

        return representation

    class Meta:
        model = Patient
        fields = '__all__'


class PatientUpdateByMedicalUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ['user', 'address', 'medicalUnit']
