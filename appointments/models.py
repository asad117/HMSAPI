# appointments/models.py
from django.db import models
import uuid
from patients.models import Patient
from providers.models import Provider
from datetime import time
from users.models import User

# appointments/models.py
# class Schedule(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
#     available_date = models.DateTimeField()
#     is_booked = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Schedule for Dr. {self.provider.last_name} on {self.available_date}"

# appointments/models.py

class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    provider = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__id': 2})  # Doctor role ID
    available_date = models.DateField()  # Date when the schedule is available
    start_time = models.TimeField(default=time(9, 0))  
    end_time = models.TimeField(default=time(13, 0))
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Schedule for Dr. {self.provider.last_name} on {self.available_date} from {self.start_time} to {self.end_time}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__id': 5}, related_name='appointments_as_patient')  # Patient role ID
    provider = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__id': 2}, related_name='appointments_as_provider')  # Doctor role ID
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Scheduled')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment with Dr. {self.provider.last_name} on {self.appointment_date}"

    # Optionally, you might want to override the delete method to ensure it's a soft delete
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

