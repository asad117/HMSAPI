# providers/admin.py
from django.contrib import admin
from .models import Provider

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'specialty', 'license_number', 'phone_number', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'specialty', 'license_number')
