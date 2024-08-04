# class AppointmentViewSet(viewsets.ModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         return Appointment.objects.filter(is_deleted=False)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             # Check if the schedule is available
#             schedule = Schedule.objects.filter(
#                 provider=serializer.validated_data['provider'],
#                 date=serializer.validated_data['appointment_date'],
#                 is_booked=False
#             ).first()

#             if not schedule:
#                 return Response(
#                     {"message": "No available schedule for this time."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Mark the schedule as booked
#             schedule.is_booked = True
#             schedule.save()

#             # Create the appointment
#             self.perform_create(serializer)
#             return Response(
#                 {"message": "Appointment created successfully", "data": serializer.data},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         if serializer.is_valid():
#             self.perform_update(serializer)
#             return Response(
#                 {"message": "Appointment updated successfully", "data": serializer.data},
#                 status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(
#             {"message": "Appointment retrieved successfully", "data": serializer.data},
#             status=status.HTTP_200_OK
#         )

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()  # Soft delete
#         return Response(
#             {"message": "Appointment deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )


from rest_framework import viewsets, permissions
from .models import Schedule, Appointment
from .serializers import ScheduleSerializer, AppointmentSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
import uuid

# class ScheduleViewSet(viewsets.ModelViewSet):
#     queryset = Schedule.objects.all()
#     serializer_class = ScheduleSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # Filter schedules based on the logged-in doctor
#         if self.request.user.role.role_name == 'Doctor':
#             return Schedule.objects.filter(provider__user=self.request.user)
#         return Schedule.objects.all()

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response(
#                 {"message": "Schedule created successfully", "data": serializer.data},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=True, methods=['get'], url_path='appointments')
#     def get_appointments(self, request, pk=None):
#         schedule = self.get_object()
#         appointments = Appointment.objects.filter(schedule=schedule)
#         serializer = AppointmentSerializer(appointments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.role_name == 'Doctor'


# class ScheduleViewSet(viewsets.ModelViewSet):
#     queryset = Schedule.objects.all()
#     serializer_class = ScheduleSerializer
#     # permission_classes = [IsDoctor]  # Only doctors can create schedules

#     def get_queryset(self):
#         # Filter schedules to show only available (not booked) schedules in the next 15 days
#         end_date = datetime.now() + timedelta(days=15)
#         return Schedule.objects.filter(is_booked=False, available_date__range=[datetime.now(), end_date])

#     # def perform_create(self, serializer):
#     #     print(self.request.user)
#     #     # Ensure that the doctor (provider) is the one creating the schedule
#     #     serializer.save(provider=self.request.user.provider)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def create(self, request, *args, **kwargs):
        # Ensure only users with the Doctor role can create schedules
        if str(request.user.role.id) != '00000000-0000-0000-0000-000000000002':  # Doctor role ID
            print(request.user.role.id)
            return Response(
                {"error": "Only doctors can create schedules."},
                status=status.HTTP_403_FORBIDDEN
    )

        return super().create(request, *args, **kwargs)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == 'Patient':
            return Appointment.objects.filter(patient__user=user, is_deleted=False)
        elif user.role.role_name == 'Doctor':
            return Appointment.objects.filter(provider__user=user, is_deleted=False)
        elif user.role.role_name == 'Admin':
            return Appointment.objects.filter(is_deleted=False)
        return Appointment.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if the schedule is already booked
            schedule = serializer.validated_data['schedule']
            if Appointment.objects.filter(schedule=schedule, status='Scheduled').exists():
                return Response({"message": "This schedule is already booked."},
                                status=status.HTTP_400_BAD_REQUEST)

            self.perform_create(serializer)
            # Mark the schedule as booked
            schedule.is_booked = True
            schedule.save()
            return Response(
                {"message": "Appointment created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {"message": "Appointment updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"message": "Appointment retrieved successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True  # Soft delete
        instance.save()
        return Response(
            {"message": "Appointment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
