import uuid
from django.db import models
from authentication.models import User
from patient.models import Patient

    # Create your models here.
class MedicalBill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medicalBill')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medicalBill')
    patientInfo = models.CharField(max_length=255)
    resultUrl = models.CharField(max_length=255)
    result = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "medicalBill"
        ordering = ["created_at"]

    def __str__(self):
        return '{}'.format(self.patient)

