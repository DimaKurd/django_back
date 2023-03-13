from rest_framework import serializers

class BingoCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True)
    words = serializers.JSONField(required=True)

class BingoEditSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True)
    words = serializers.JSONField(required=True)

class BingoResponseSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200)