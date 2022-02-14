import typing

from rest_framework_jwt.settings import api_settings

from user.models import CustomUser


def create_token(user: CustomUser) -> typing.AnyStr:
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    data = {'token': token}
    return data
