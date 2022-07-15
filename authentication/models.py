import uuid
from django.db import models

# Create your models here.

from django.db import models

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

class UserManager(BaseUserManager):

    def create_user(self, username, email, roler, password=None ):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email), roler=roler)
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
#     ROLER_CHOISE = (
#         ("roler1", "Contractor management"),
#         ('roler2', "General contractor"),
#         ("roler3", "Group management"),
#         ("roler4", "Group in general"),
#         ("roler5", "User" )
#     )
#     roler = models.CharField(max_length=30, choices=ROLER_CHOISE, default="roler5")
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
#     def is_roler1(self):
#         return self.roler== "roler1"

#     @property
#     def is_roler5(self):
#         return self.roler == "roler5"

#     @property
#     def is_roler3(self):
#         return self.roler == "roler3"
class User(AbstractBaseUser,PermissionsMixin):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    ROLE_CHOICE = (
        ("roler1", "Doctor"),
        ('roler2', "Patient"),
        ("roler3", "Medical Unit"),
        ("roler4", "Admin"),
    )
    roler = models.CharField(max_length=30, choices=ROLE_CHOICE)
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
