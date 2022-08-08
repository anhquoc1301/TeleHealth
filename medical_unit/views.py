from django.shortcuts import get_object_or_404
from pkg_resources import require
from address.models import Address
from authentication.serializer import RegisterSerializer
from doctor.models import Doctor
from doctor.serializers import DoctorSerializer
from patient.models import Patient
from patient.serializers import PatientDetailSerializer, PatientSerializer, PatientUpdateByMedicalUnitSerializer
from patient_management.models import PatientManagement
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from authentication.mixins import GetSerializerClassMixin
from .models import MedicalUnit
from .serializers import MedicalUnitSerializer, PatientRegisterSerializer
from rest_framework import generics, status, permissions
from base.message import success, error

from authentication.models import User
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from authentication.permissions import Role1, Role2, Role3, Role4, Role1or3
from django.db import transaction


class MedicalUnitViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = MedicalUnit.objects.all()
    permission_classes = [Role3]
    permission_classes_by_action = {
        'detailPatientByMedicalUnit': [Role1or3]
    }
    serializer_class = MedicalUnitSerializer
    serializer_action_classes = {
        'addPatientByMedicalUnit': PatientRegisterSerializer,
        'updatePatientByMedicalUnit': PatientUpdateByMedicalUnitSerializer,
    }

    def create(self, request):
        userData = request.data['user']
        medicalData = request.data['medical']
        userSerializer = RegisterSerializer(data=userData)
        if userSerializer.is_valid():
            newUser = User.objects.create_user(
                email=userData['email'], password=userData['password'], username=userData['username'], phone=userData['phone'], Role=userData['Role'])
            medicalData['user'] = newUser.id
            medicalSerializer = self.get_serializer(data=medicalData)
            if medicalSerializer.is_valid():
                medicalSerializer.save()
                return success(data=medicalSerializer.data)
        return error()

    @action(
        methods=["POST"],
        detail=False,
        url_path="add_patient"
    )
    @transaction.atomic
    def addPatientByMedicalUnit(self, request):
        try:
            medicalUnitId = request.user.id
            if medicalUnitId:
                medicalUnit = get_object_or_404(
                    MedicalUnit, user_id=medicalUnitId)
                patientData = request.data
                serializer = self.get_serializer(data=patientData)
                if serializer.is_valid():
                    user = User.objects.create_user(
                        email=patientData['email'],
                        password=patientData['password'],
                        username=patientData['username'],
                        phone=patientData['phone'],
                        role='role2',
                    )
                    address = Address.objects.create(
                        country_id=patientData['country'],
                        province_id=patientData['province'],
                        district_id=patientData['district'],
                        ward_id=patientData['ward'],
                    )
                    patient = Patient.objects.create(
                        name=patientData['name'],
                        gender=patientData['gender'],
                        unsignedName=patientData['unsignedName'],
                        dateOfBirth=patientData['dateOfBirth'],
                        insuranceCode=patientData['insuranceCode'],
                        identification=patientData['identification'],
                        contact=patientData['contact'],
                        ethnic_id=patientData['ethnic'],
                        medicalUnit_id=medicalUnit.id,
                        address_id=address.id,
                        user_id=user.id,
                    )
                    transaction.atomic()
                    patientSerializer = PatientSerializer(patient)
                    return success(data=patientSerializer.data)
                else:
                    return error(data='data not valid')
            else:
                return error(data='user not exist')
        except:
            transaction.rollback()
            return error(data='error')

    @action(
        methods=["GET"],
        detail=False,
        url_path="list_patient_by_medical_unit"
    )
    def listPatientByMedicalUnit(self, request):
        medicalUnitId = request.user.id
        if medicalUnitId:
            medicalUnit = get_object_or_404(MedicalUnit, user_id=medicalUnitId)
            patients = Patient.objects.filter(medicalUnit=medicalUnit)
            dataFilter = self.request.GET.get('dataFilter')
            if dataFilter != 'null':
                patients = patients.filter(
                    Q(name=dataFilter) | Q(gender=dataFilter))
            patientsSerializer = PatientSerializer(patients, many=True)
            return Response(data=patientsSerializer.data, status=status.HTTP_200_OK)
        else:
            return error(data='user not exist')

    def detailPatientByMedicalUnit(self, request, *args, **kwargs):
        patientId = self.request.GET.get('pk')
        patient = Patient.objects.get(id=patientId)
        patientSerializer = PatientDetailSerializer(patient)
        return Response(data=patientSerializer.data, status=status.HTTP_200_OK)

    def updatePatientByMedicalUnit(self, request, *args, **kwargs):
        patientId = self.request.GET.get('pk')
        patient = Patient.objects.get(id=patientId)
        patientSerializer = self.get_serializer(
            instance=patient, data=request.data, partial=True)
        try:
            patientSerializer.is_valid(raise_exception=True)
            self.perform_update(patientSerializer)
            return success(data=patientSerializer.data)
        except:
            return error(data="Not valid data")

    @action(
        methods=["GET"],
        detail=False,
        url_path="list_doctor_wait_accept_by_medical_unit"
    )
    def listDoctorWaitAcceptByMedicalUnit(self, request, *args, **kwargs):
        medicalUnit = MedicalUnit.objects.get(user=request.user.id)
        doctors = Doctor.objects.filter(
            Q(medicalUnit=medicalUnit) & Q(is_accept=False))
        doctorsSerializer = DoctorSerializer(doctors, many=True)
        return Response(data=doctorsSerializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path="list_doctor_by_medical_unit"
    )
    def listDoctorByMedicalUnit(self, request, *args, **kwargs):
        medicalUnit = MedicalUnit.objects.get(user=request.user.id)
        doctors = Doctor.objects.filter(
            Q(medicalUnit=medicalUnit) & Q(is_accept=True))
        dataFilter = self.request.GET.get('dataFilter')
        if dataFilter != 'null':
            doctors = doctors.filter(Q(name=dataFilter) | Q(gender=dataFilter))
        doctorsSerializer = DoctorSerializer(doctors, many=True)
        return Response(data=doctorsSerializer.data, status=status.HTTP_200_OK)

    def acceptDoctorWaitAcceptByMedicalUnit(self, request, *args, **kwargs):
        doctorId = self.request.GET.get('pk')
        doctor = Doctor.objects.get(id=doctorId)
        doctor.is_accept = True if doctor.is_accept == False else False
        doctor.save()
        return Response(data=doctor.is_accept, status=status.HTTP_200_OK)
