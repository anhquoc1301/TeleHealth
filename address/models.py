from statistics import mode
import uuid
from django.db import models
from authentication.models import User

# Create your models here.


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    unsignedName = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "country"
        ordering = ["created_at"]

    def __str__(self):
        return '{}'.format(self.name)


class Province(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    unsignedName = models.CharField(max_length=200)
    country= models.ForeignKey(Country, on_delete=models.CASCADE, related_name='province')

    
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "province"
        ordering = ["created_at"]

    def __str__(self):
        return '{}'.format(self.name)

class District(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    unsignedName = models.CharField(max_length=200)
    province= models.ForeignKey(Province, on_delete=models.CASCADE, related_name='district')

    
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "district"
        ordering = ["created_at"]

    def __str__(self):
        return '{}'.format(self.name)

class Ward(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    unsignedName = models.CharField(max_length=200)
    district= models.ForeignKey(District, on_delete=models.CASCADE, related_name='ward')

    
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ward"
        ordering = ["created_at"]

    def __str__(self):
        return '{}'.format(self.name)

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="address")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="address")
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="address")
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="address")

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "address"
        ordering = ["created_at"]


class Ethnic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    unsignedName = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ethnic"
        ordering = ["created_at"]

    def __str__(self):
        return '{}'.format(self.name)