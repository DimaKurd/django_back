from rest_framework import serializers


class UserSessionDataSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=True)
    game_id = serializers.IntegerField(required=True)
    player_id = serializers.IntegerField(required=True)
    progress = serializers.JSONField()
    random_seed = serializers.IntegerField(required=True)


class UserSessionsDataSerializer(serializers.ListSerializer):
    child = UserSessionDataSerializer


class UserSessionEndpointResponse(serializers.Serializer):
    status = serializers.CharField(max_length=200)


class UserSessionUpdateProgressSerializer(serializers.Serializer):
    progress = serializers.JSONField()
