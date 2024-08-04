from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, DoctorProfile, PatientProfile, AdminProfile, OtherStaffProfile

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         role = instance.role.role_name
#         if role == 'Doctor':
#             DoctorProfile.objects.create(user=instance)
#         elif role == 'Patient':
#             PatientProfile.objects.create(user=instance)
#         elif role == 'Admin':
#             AdminProfile.objects.create(user=instance)
#         else:
#             OtherUserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     role = instance.role.role_name
#     if role == 'Doctor':
#         instance.doctorprofile.save()
#     elif role == 'Patient':
#         instance.patientprofile.save()
#     elif role == 'Admin':
#         instance.adminprofile.save()
#     else:
#         instance.otheruserprofile.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role.role_name == 'Doctor':
            DoctorProfile.objects.create(user=instance)
        elif instance.role.role_name == 'Patient':
            PatientProfile.objects.create(user=instance)
        elif instance.role.role_name == 'Admin':
            AdminProfile.objects.create(user=instance)
        else:
            OtherStaffProfile.objects.create(user=instance)
