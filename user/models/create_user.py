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
from rest_framework_jwt.settings import api_settings

from django.core.exceptions import ObjectDoesNotExist
from user.tasks import send_create_user_code

from user.models import CustomUser


class CreateUserManager(models.Manager):
    def get_for_activating(self):
        return super().get_queryset().filter(activated=False)


class CreateUser(models.Model):
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
        activation_frontend_url = '{}{}/{}/activation/'.format(settings.FRONTEND_URL, 'user/create_user', self.uuid)
        text = 'Your url for create account - {}'.format(activation_frontend_url)
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
        self.clean()
        self.activated = True
        self.save()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        user = CustomUser.objects.create_user(username=self.username,
                                              password=self.password,
                                              email=self.email)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        data = {'token': token}
        return data

    def clean(self):
        if self.sent_at + timedelta(minutes=10) < now():
            raise ValidationError('Your token was expired')
        try:
            CustomUser.objects.get(email=self.email)
            raise ValidationError('Your email have already busy')
        except ObjectDoesNotExist:
            pass



@receiver(post_save, sender=CreateUser)
def send_reset_password_code_signal(sender, instance, **kwargs):
    CreateUser.objects.filter(username=instance.username).exclude(pk=instance.pk).delete()
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
