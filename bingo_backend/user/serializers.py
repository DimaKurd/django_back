from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    # user_id = serializers.IntegerField(read_only=True)
    nickname = serializers.CharField(max_length=40, required=True)
    # role = serializers.IntegerField(required=True, read_only=True)
    password = serializers.CharField(max_length=40, required=True)

class GuestSerializer(serializers.Serializer):
    # user_id = serializers.IntegerField(read_only=True)
    nickname = serializers.CharField(max_length=40, required=True)
    # role = serializers.IntegerField(required=True, read_only=True)

class RoleSerializer(serializers.Serializer):
    role_id = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=40, required=True)