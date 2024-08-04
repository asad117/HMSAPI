# users/admin.py
from django.contrib import admin
from .models import Role, User

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'created_at', 'updated_at')
    search_fields = ('role_name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'role','is_active', 'created_at', 'updated_at')
    search_fields = ('username', 'email')
    list_filter = ('role',)
