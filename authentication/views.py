from django.shortcuts import render
from rest_framework import generics, status, permissions
from .serializer import RegisrerSerializer, LoginSerializer, LogoutSerializer, ChangePasswordSerializer, GetUserReadOnlySerializer


from  rest_framework_simplejwt.tokens import RefreshToken
from .models import User

from .mixins import GetSerializerClassMixin
from apartment.message import sucsess,error

# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisrerSerializer
    def post(self, request):
        user = request.data
        # try:
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()
            return sucsess(data=serializer.data)
        return error(data=serializer.errors)
        # except:
        #     return error()


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                print(serializer)
                return sucsess(data=serializer.data)
            return error(data=serializer.errors)
        except(error):
            print(error)
            return error("Sign in failed", data='')



class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return sucsess("Logout success",'')
            return error(data=serializer.errors)
        except:
            return error("Sign out failed", data='')


class Change_passwordAPIview(generics.GenericAPIView, GetSerializerClassMixin):

    serializer_class = ChangePasswordSerializer

    permission_classes =[permissions.IsAuthenticated]


    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = request.user
                if not user.check_password(serializer.validated_data["old_password"]):
                    return error('old password is not correct','')
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                serializer = GetUserReadOnlySerializer(user)
                return sucsess(data=serializer.data)
            return error(data=serializer.errors)
        except:
            return error("Change password failed", data='')



