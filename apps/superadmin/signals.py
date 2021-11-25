from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.superadmin.models import *
from apps.human_resource.models import *


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_associate_tables(sender, instance, created, **kwargs):
    if created:
        print(instance)
        EmployeeProfile.objects.create(employee=instance)
        EmploymentInformation.objects.create(employee=instance)
        PaymentInformation.objects.create(employee=instance)
        EmergencyInformation.objects.create(employee=instance)

try:
    if len(Role.objects.all()) < 4:
        Role.objects.create(name="super_admin")
        Role.objects.create(name="human_resources")
        Role.objects.create(name="subordinate_staff")
        Role.objects.create(name="finance")
except:
    print("Roles does not exist yet")

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key),
        'token':reset_password_token.key
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Fuzu pay admin"),
        # message:
        email_plaintext_message,
        # from:
        "ken.mbira@student.moringaschool.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
