# providers/models.py
from django.db import models
import uuid
from users.models import User
from django.core.validators import MinLengthValidator, RegexValidator

class Provider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    specialty = models.CharField(max_length=255)
    license_number = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=50, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"
