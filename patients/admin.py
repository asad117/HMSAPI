# patients/admin.py
from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'address', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'phone_number')
