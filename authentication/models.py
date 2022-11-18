import uuid
from django.db import models

# Create your models here.

from django.db import models

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

class UserManager(BaseUserManager):

    def create_user(self, username, email, role, phone, password=None ):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email),phone=phone, role=role)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


# class User(AbstractBaseUser,PermissionsMixin):
#     username = models.CharField(max_length=255, unique=True, db_index=True)
#     email = models.EmailField(max_length=255, unique=True, db_index=True)
#     Role_CHOISE = (
#         ("Role1", "Contractor management"),
#         ('Role2', "General contractor"),
#         ("Role3", "Group management"),
#         ("Role4", "Group in general"),
#         ("Role5", "User" )
#     )
#     Role = models.CharField(max_length=30, choices=Role_CHOISE, default="Role5")
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     objects = UserManager()

#     def __str__(self):
#         return self.email

#     def tokens(self):
#         refresh = RefreshToken.for_user(self)
#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token)
#         }

#     @property
#     def is_Role1(self):
#         return self.Role== "Role1"

#     @property
#     def is_Role5(self):
#         return self.Role == "Role5"

#     @property
#     def is_Role3(self):
#         return self.Role == "Role3"
class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    ROLE_CHOICE = (
        ("role1", "Doctor"),
        ('role2', "Patient"),
        ("role3", "Medical Unit"),
        ("role4", "Admin"),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICE, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
