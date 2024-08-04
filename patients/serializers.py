from rest_framework import serializers
from .models import Patient
from users.models import User

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Patient
        fields = '__all__'
