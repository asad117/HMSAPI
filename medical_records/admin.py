# medical_records/admin.py
from django.contrib import admin
from .models import MedicalRecord

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'diagnosis', 'treatment', 'medication', 'created_at', 'updated_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'provider__first_name', 'provider__last_name', 'diagnosis')
