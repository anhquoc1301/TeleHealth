
from rest_framework import serializers
from .models import ResultFile, UserUploadedFile



class UserUploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUploadedFile
        fields = '__all__'

class ResultFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultFile
        fields = '__all__'
# class PatientReadOnlyDoctorSerializer(serializers.ModelSerializer):
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         try:
#             patient=Patient.objects.get(id=instance.patient.id)
#             patientInfo = PatientSerializer(patient).data
#         except:
#             patientInfo = ""

#         representation['patient'] = patientInfo

#         return representation
#     class Meta:
#         model = PatientManagement
#         fields = '__all__'
# class DoctorReadOnlyDoctorSerializer(serializers.ModelSerializer):
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         try:
#             doctor=Doctor.objects.get(id=instance.doctor.id)
#             doctorInfo = DoctorSerializer(doctor).data
#         except:
#             doctorInfo = ""

#         representation['doctor'] = doctorInfo

#         return representation
#     class Meta:
#         model = PatientManagement
#         fields = '__all__'