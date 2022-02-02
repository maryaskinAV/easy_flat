import uuid
import traceback


from django.conf import settings
from django.db.models.signals import post_save
from django.db import models
from django.db.transaction import atomic
from django.dispatch import receiver
from django.utils.timezone import now,timedelta
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework_jwt.settings import api_settings

from user.tasks import send_create_user_code
from user.models import CustomUser
from user.service import create_token

class CreateUserManager(models.Manager):
    def get_for_activating(self):
        return super().get_queryset().filter(activated=False)


class SignUpOrder(models.Model):
    """
    Модель заявки на регистрацию пользователя
    """
    email = models.EmailField()
    sent_at = models.DateTimeField(default=now)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    username = models.CharField(max_length=200)
    activated = models.BooleanField(default=False)
    objects = CreateUserManager()
    error_response = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=16)

    def send(self):
        """ Send email with activation url. """
        self.clean()
        try:
            self.send_email()
            self.sent_at = now()
        except Exception:
            self.error_response = traceback.format_exc()
            self.save()

    def send_email(self):
        title = 'Easy Flat - activation code'
        activation_url = f'{settings.FRONTEND_URL}user/create_user/{self.uuid}/activation/'
        text = f'Your url for create account - {activation_url}'
        response = send_mail(
            title,
            text,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=True
        )
        return response

    @atomic
    def activate(self):
        self.activated = True
        self.save()
        user = CustomUser.objects.create_user(username=self.username,
                                              password=self.password,
                                              email=self.email)
        token = create_token(user)
        return token

    def clean(self):
        """
        Токен действует не более 10 минут. При просроченном токене регистрация невозможна
        """
        if self.sent_at + timedelta(minutes=10) < now():

            raise ValidationError('Your token was expired')
        if CustomUser.objects.filter(email=self.email).exists():
            raise ValidationError('Your email have already busy')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


@receiver(post_save, sender=SignUpOrder)
def send_reset_password_code_signal(sender, instance:SignUpOrder, **kwargs):
    SignUpOrder.objects.filter(username=instance.username).exclude(pk=instance.pk).delete()
    if instance.activated:
        title = 'Easy Flat - activation success'
        text = 'Your account was activated'
        send_mail(title,
                  text,
                  settings.EMAIL_HOST_USER,
                  [instance.email],
                  fail_silently=True)
    else:
        send_create_user_code(instance.id)
