import uuid

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.timezone import now, timedelta
from django.db.transaction import atomic
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from rest_framework_jwt.settings import api_settings

from user.tasks import send_reset_password_code

class PasswordChangeOrderManager(models.Manager):
    def get_for_activating(self):
        return super().get_queryset().filter(activated=False)


class PasswordChangeOrder(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    password = models.CharField(max_length=16)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    error_response = models.TextField(null=True, blank=True)
    sent_at = models.DateTimeField(default=now)
    activated = models.BooleanField(default=False)
    objects = PasswordChangeOrderManager()

    def send(self):
        """ Send email with activation url. """
        self.clean()
        try:
            self.send_email()
        except Exception:
            self.error_response = traceback.format_exc()
            self.save()

    def send_email(self):
        title = 'Easy Flat - activation password'
        activation_frontend_url = '{}{}/{}/activation/'.format(settings.FRONTEND_URL, 'user/change_password', self.uuid)
        text = 'Your url for activate password - {}'.format(activation_frontend_url)
        response = send_mail(
            title,
            text,
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=True
        )
        return response

    @atomic
    def activate(self):
        self.clean()
        self.activated = True
        user = self.user
        user.set_password(self.password)
        user.save()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        data = {'token': token}
        return data

    def clean(self):
        if self.sent_at + timedelta(minutes=10) < now():
            raise ValidationError('Your token was expired')



@receiver(post_save, sender=PasswordChangeOrder)
def send_reset_password_code_signal(sender, instance, **kwargs):
    PasswordChangeOrder.objects.filter(user=instance.user).exclude(pk=instance.pk).delete()
    if instance.activated:
        title = 'Easy Flat - activation success'
        text = 'Your password was activated'
        send_mail(title,
                  text,
                  settings.EMAIL_HOST_USER,
                  [instance.user.email],
                  fail_silently=True)
    else:
        send_reset_password_code(instance.id)
