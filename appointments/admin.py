# appointments/admin.py
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'appointment_date', 'status', 'created_at', 'updated_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'provider__first_name', 'provider__last_name')
    list_filter = ('status',)
