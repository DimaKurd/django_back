from rest_framework import serializers


class WordSerializer(serializers.Serializer):
    word = serializers.CharField(required=True)

class BingoCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True)
    words = serializers.ListField(required=True)


class BingoEditSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True)
    words = serializers.ListField(required=True)


class BingoResponseSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200)


class BingoDataSerializer(serializers.Serializer):
    bingo_id = serializers.IntegerField(required=True)
    author_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    words = serializers.ListField(child=WordSerializer(), required=True)


class BingoObjectsArraySerializer(serializers.Serializer):
    user_bingos = serializers.ListField(child=BingoDataSerializer())




