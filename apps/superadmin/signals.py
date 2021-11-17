from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from apps.superadmin.models import *




@receiver(post_save, sender=User)
def create_associate_tables(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(employee=instance)
        group = Group.objects.get(name='subordinate_staff') 
        group.user_set.add(instance)
        instance.save()
        # EmploymentInformation.objects.create(employee=instance)
        # PaymentInformation.objects.create(employee=instance)
        # EmergencyInformation.objects.create(employee=instance)

if len(Group.objects.all()) < 3:
    Group.objects.create(name="super_admin")
    Group.objects.create(name="human_resources")
    Group.objects.create(name="subordinate_staff")
