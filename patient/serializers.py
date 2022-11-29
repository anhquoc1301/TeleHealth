
from authentication.models import User
from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class PatientDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            user=User.objects.get(id=instance.user.id)
            patientEmail = user.email
            patientPhone = user.phone
        except:
            patientEmail = ''
            patientPhone = ''

        representation['email'] = patientEmail
        representation['phone'] = patientPhone

        return representation
    class Meta:
        model = Patient
        fields = '__all__'

class PatientUpdateByMedicalUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ['user', 'address', 'medicalUnit']