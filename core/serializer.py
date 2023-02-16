from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

from rest_framework import serializers
from store.models import Customer


class UserCreateSerializer(BaseUserCreateSerializer):

    def create(self, validated_data):
        user = super().create(validated_data)
        print(validated_data)
        cstmr = Customer.objects.create(first_name=user.first_name, last_name=user.last_name, user=user)
        cstmr.save()
        return user

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']


class UserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
