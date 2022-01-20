from django.test import TestCase

from django.shortcuts import reverse
from unittest.mock import patch

from user.models import SignUpOrder, CustomUser, PasswordChangeOrder
from user.tasks import send_create_user_code,send_reset_password_code
from user.service import create_token

class BaseTestCase(TestCase):
    first_password = '123'

    def setUp(self):
        super().setUp()
        self.admin_user = CustomUser.objects.create(username='admin', email="dkdjjdkd@mail.ru",
                                                    is_active=True, is_staff=True,
                                                    is_superuser=True)
        self.admin_user.set_password(self.first_password)
        self.admin_user.save()

        self.quest = CustomUser.objects.create(username='quest', email="dkdjjdkd@mail.ru",
                                               is_active=True, is_staff=True, is_superuser=False)
        self.quest.set_password(self.first_password)
        self.quest.save()


class MockSMTP_SSL:
    '''
    Mock object for smtplib.SMTP_SSL
    '''

    def __init__(self):
        super().__init__()

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def login(self, email, passsword):
        pass


class MockSMTPSSLSuccess(MockSMTP_SSL):

    def sendmail(self, *args, **kwargs):
        return 1


class MockSMTPSSLError(MockSMTP_SSL):
    def sendmail(self, *args, **kwargs):
        raise KeyError('Exception')


class MockSMTPSSLFail(MockSMTP_SSL):
    def sendmail(self, *args, **kwargs):
        return


class UserTestCase(BaseTestCase):

    @patch('smtplib.SMTP_SSL')
    def test_create_user(self, smtp_mock):
        smtp_mock.return_value.__enter__.return_value = MockSMTPSSLSuccess()
        order = SignUpOrder.objects.create(username=self.admin_user, uuid='cdfab639-fb06-43d8-a09d-1f3452f1b08d', email='example@gmail.com')
        send_create_user_code(order.id)
        order.refresh_from_db()
        self.assertIsNotNone(order.sent_at)

    @patch('smtplib.SMTP_SSL')
    def test_reset_password(self, smtp_mock):
        smtp_mock.return_value.__enter__.return_value = MockSMTPSSLSuccess()

        order = PasswordChangeOrder.objects.create(user=self.admin_user, uuid='cdfab639-fb06-43d8-a09d-1f3452f1b08d')
        send_reset_password_code(order.id)
        order.refresh_from_db()
        self.assertIsNotNone(order.sent_at)

    def test_create_token(self):
        token = create_token(self.admin_user)

"""
Приоритеты: 
1. ТО что может сломаться (платежка,деньги)
2. Корневые функции 
3. 
"""
#todo покрыть тестами создание модели