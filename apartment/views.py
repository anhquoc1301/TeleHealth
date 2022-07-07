from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Apartment
from .serializers import ApartmentSerializer, CreateApartmentSerializer, UpdateApartmentSerializer
from django.db.models import Q
from .pagination import CustomNumberPagination
#Them
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from .message import error,sucsess
from expenses.permissions import IsOwner, Roler5,Roler2,Roler3
from authentication.models import User


# Modelviewset
class ApartmentViewSet(viewsets.ModelViewSet,):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    pagination_class = CustomNumberPagination
    permission_classes = [permissions.IsAuthenticated]


class ApartmentView(generics.ListAPIView, APIView, CustomNumberPagination):
    pagination_class = CustomNumberPagination
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    serializer_action_classes = {
        "post": ApartmentSerializer,
        "list": ApartmentSerializer,
        "put": UpdateApartmentSerializer,
    }
    permission_classes = [permissions.IsAuthenticated , Roler3]

    filter_backends = [DjangoFilterBackend , filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['manage_id', 'apartment_add', 'customer_name']
    ordering_fields = ['manage_id', 'apartment_add', 'id']
    filter_fields = ('manage_id', 'customer_name', 'apartment_add')

    def get(self, request, id=None, *args, **kwargs):
        try:
            if id:
                queryset = Apartment.objects.filter(id=id)
                self.check_object_permissions(request, request.user.is_roler1)
                serializer = ApartmentSerializer(queryset, many=True)
                return sucsess(data=serializer.data)

            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response({
                        "data": serializer.data,
                        "success": True
                    })

            serializer = self.get_serializer(queryset, many=True)
            return sucsess(data=serializer.data)
        except:
            return error("Get apartment fail")

    def post(self, request):

        serializer = self.serializer_action_classes.get('post')(data=request.data)
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        self.check_object_permissions(request, user_id)
        if not user:
            return error('No users','')

        try:
            if user_id:
                request.data["user"] = user_id
                request.data["updated_user_id"] = user_id
                request.data["created_user_id"] = user_id
                request.data["created_user_name"] = user.username
                request.data["updated_user_name"] = user.username
            if serializer.is_valid():
                serializer.save()
                return sucsess(data=serializer.data)
            return error(data=serializer.errors)
        except:
            return error("Unable to create apartment")

    def delete(self, request, id):
        try:
            apartment =get_object_or_404(Apartment, id=id)
            user_id = request.user.id
            self.check_object_permissions(request, user_id)
            apartment.delete()
            return sucsess(message="Delete sucssesfull")
        except:
            return error("Unable to delete apartment")

    def put(self, request, id=None):
        try:
            apartment =get_object_or_404(Apartment, id=id)

            self.check_object_permissions(request, apartment)
            serializer = self.serializer_action_classes.get('put')(instance=apartment, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return sucsess("update apartment sucssesful",data=serializer.data)
            return error(data=serializer.errors)
        except:
            return error("Update apartment fail")