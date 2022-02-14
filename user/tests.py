import typing
from unittest.mock import MagicMock, patch

from django.test import TestCase

from user.models import CustomUser, PasswordChangeOrder, SignUpOrder
from user.service import create_token
from user.tasks import send_create_user_code, send_reset_password_code


class BaseTestCase(TestCase):
    first_password = "123"

    def setUp(self) -> None:
        super().setUp()
        self.admin_user = CustomUser.objects.create(
            username="admin",
            email="dkdjjdkd@mail.ru",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        self.admin_user.set_password(self.first_password)
        self.admin_user.save()

        self.quest = CustomUser.objects.create(
            username="quest",
            email="dkdjjdkd@mail.ru",
            is_active=True,
            is_staff=True,
            is_superuser=False,
        )
        self.quest.set_password(self.first_password)
        self.quest.save()


class MockSMTP_SSL:
    """
    Mock object for smtplib.SMTP_SSL
    """

    def __init__(self) -> None:
        super().__init__()

    def __enter__(self, *args: typing.Any, **kwargs: typing.Any):
        return self

    def __exit__(
        self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any
    ) -> None:
        pass

    def login(self, email: typing.AnyStr, passsword: typing.AnyStr) -> None:
        pass


class MockSMTPSSLSuccess(MockSMTP_SSL):
    def sendmail(self, *args: typing.Any, **kwargs: typing.Any) -> int:
        return 1


class MockSMTPSSLError(MockSMTP_SSL):
    def sendmail(self, *args: typing.Any, **kwargs: typing.Any) -> Exception:
        raise KeyError("Exception")


class MockSMTPSSLFail(MockSMTP_SSL):
    def sendmail(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        return


class UserTestCase(BaseTestCase):
    @patch("smtplib.SMTP_SSL")
    def test_create_user(self, smtp_mock: MagicMock) -> None:
        smtp_mock.return_value.__enter__.return_value = MockSMTPSSLSuccess()
        order = SignUpOrder.objects.create(
            username=self.admin_user, email="example@gmail.com"
        )
        send_create_user_code(order.id)
        order.refresh_from_db()
        self.assertIsNotNone(order.sent_at)

    @patch("smtplib.SMTP_SSL")
    def test_reset_password(self, smtp_mock: MagicMock) -> None:
        smtp_mock.return_value.__enter__.return_value = MockSMTPSSLSuccess()
        order = PasswordChangeOrder.objects.create(
            user=self.admin_user, uuid="cdfab639-fb06-43d8-a09d-1f3452f1b08d"
        )
        send_reset_password_code(order.id)
        order.refresh_from_db()
        self.assertIsNotNone(order.sent_at)

    def test_create_token(self) -> None:
        token = create_token(self.admin_user)
