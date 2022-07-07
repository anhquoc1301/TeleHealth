from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
from rest_framework import generics, status, permissions
from apartment.message import error,sucsess

from authentication.models import User
from apartment.pagination import CustomNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from expenses.permissions import Roler3,Roler5, Roler1


class CompanyViewset(viewsets.ModelViewSet, CustomNumberPagination):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['company_name', 'address_company']
    ordering_fields = ['company_name', 'address_company', 'id']
    filter_fields = ('company_name', 'address_company', 'id')

    permission_classes_by_action = {
        'list': [AllowAny],
        "create": [permissions.IsAuthenticated],
        "retrieve": [Roler1|Roler3],
        "update": [Roler5],
        "destroy": [Roler3],
    }

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            total_items = self.request.GET.get('total_items')
            if total_items is not None:
                queryset = queryset[:int(total_items)]

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return sucsess(data=serializer.data)

        except:
            return error("Get company fail")


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            # self.check_object_permissions(request, user_id)
            if not user:
                return error('No users', '')

            if user_id:
                request.data["user"] = user_id
                request.data["updated_user_id"] = user_id
                request.data["created_user_id"] = user_id
                request.data["created_user_name"] = user.username
                request.data["updated_user_name"] = user.username
            if serializer.is_valid():
                self.perform_create(serializer)
                return sucsess(data=serializer.data)
            else:
                return error(data=serializer.errors)
        except:
            return error("Get company fail")

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return sucsess(data=serializer.data)
        except:
            return error("Get company detail fail")

    def destroy(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            instance = Company.objects.get(id=pk)
            self.perform_destroy(instance)
            return sucsess('delete sucsess', data="")
        except:
            return error("delete company fail")

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

