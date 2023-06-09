from rest_framework import serializers


class GameEndpointResponseSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200)


class SingleGameDataResponse(serializers.Serializer):
    game_id = serializers.IntegerField(required=True)
    bingo_id = serializers.IntegerField(required=True)
    launched = serializers.BooleanField(required=True)
    max_players = serializers.IntegerField(required=False)


class ManyGameDataResponse(serializers.ListSerializer):
    child = SingleGameDataResponse()


class GameCreationDataSerializer(serializers.Serializer):
    bingo_id = serializers.IntegerField(required=True)


class GameConnectDataSerializer(serializers.Serializer):
    join_code = serializers.CharField(required=True, max_length=8)
