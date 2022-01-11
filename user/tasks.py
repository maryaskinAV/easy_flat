from celery import shared_task
from django.apps import apps


@shared_task
def send_create_user_code(code_id):
    user = apps.get_model('user.CreateUser')
    code = user.objects.get(id=code_id)
    code.send()


@shared_task
def send_reset_password_code(code_id):
    user = apps.get_model('user.PasswordChangeOrder')
    code = user.objects.get(id=code_id)
    code.send()


