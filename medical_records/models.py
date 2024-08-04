# medical_records/models.py
from django.db import models
import uuid
from patients.models import Patient
from providers.models import Provider

class MedicalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    medication = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Record for {self.patient.first_name} {self.patient.last_name} by Dr. {self.provider.last_name}"
