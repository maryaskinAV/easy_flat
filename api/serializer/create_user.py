from rest_framework import serializers
from user.models import CreateUser


class CreateUserSerializers(serializers.ModelSerializer):

    class Meta:
        fields = ['email', 'username', 'password']
        model = CreateUser
