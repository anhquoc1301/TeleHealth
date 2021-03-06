import uuid
from django.db import models
from address.models import Address, Ethnic
from authentication.models import User
from medical_unit.models import MedicalUnit
    # Create your models here.
class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    GENDER_CHOISE = (
        ("man", "Man"),
        ('woman', "Woman"),
    )
    gender = models.CharField(choices=GENDER_CHOISE, max_length=20)
    unsignedName = models.CharField(max_length=200)
    medicalUnit = models.ForeignKey(MedicalUnit, on_delete=models.CASCADE, related_name='patient')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='patient')
    ethnic = models.ForeignKey(Ethnic, on_delete=models.CASCADE, related_name='patient')
    dateOfBirth = models.DateField()
    insuranceCode = models.CharField(max_length=20)
    identification = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient")


    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "patient"
        ordering = ["created_at"]

    def __str__(self):
        return '{}'.format(self.name)

