from django.shortcuts import render
from rest_framework import viewsets
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
