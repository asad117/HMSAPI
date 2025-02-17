# Generated by Django 5.0.7 on 2024-07-28 17:53

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('appointment_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Scheduled', max_length=50)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='providers.provider')),
            ],
        ),
    ]
