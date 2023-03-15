from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=40, required=True)
    password = serializers.CharField(max_length=40, required=True)


class GuestSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=40, required=True)


class UserResponseSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200)
