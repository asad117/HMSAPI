# # appointments/serializers.py
# from rest_framework import serializers
# from .models import Schedule, Appointment

# class ScheduleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Schedule
#         fields = '__all__'

# class AppointmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Appointment
#         fields = '__all__'


# schedules/serializers.py
from rest_framework import serializers
from .models import Schedule
from appointments.models import Appointment

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

# class AppointmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Appointment
#         fields = '__all__'
        
#     def create(self, validated_data):
#         schedule = Schedule.objects.get(id=validated_data['schedule'].id)
#         if schedule.is_booked:
#             raise serializers.ValidationError("This time slot is already booked.")
        
#         appointment = Appointment.objects.create(**validated_data)
#         schedule.is_booked = True
#         schedule.save()
        
#         return appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        
    def create(self, validated_data):
        schedule = Schedule.objects.get(id=validated_data['schedule'].id)
        if schedule.is_booked:
            raise serializers.ValidationError("This time slot is already booked.")
        
        appointment = Appointment.objects.create(**validated_data)
        schedule.is_booked = True
        schedule.save()
        
        return appointment