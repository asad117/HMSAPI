# users/management/commands/create_roles.py

from django.core.management.base import BaseCommand
from users.models import Role

class Command(BaseCommand):
    help = 'Create default roles with specific IDs'

    def handle(self, *args, **kwargs):
        roles = [
            (1, 'Admin'),
            (2, 'Doctor'),
            (3, 'Nurse'),
            (4, 'Receptionist'),
            (5, 'Patient')
        ]

        for role_id, role_name in roles:
            role, created = Role.objects.get_or_create(id=role_id, defaults={'role_name': role_name})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role "{role_name}" created successfully with ID {role_id}.'))
            else:
                self.stdout.write(f'Role "{role_name}" with ID {role_id} already exists.')


# python manage.py create_roles