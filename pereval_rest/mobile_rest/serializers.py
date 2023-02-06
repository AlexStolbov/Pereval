from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, allow_blank=False)
    fam = serializers.CharField(allow_blank=True)
    name = serializers.CharField(allow_blank=True)
    otc = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)


class CoordsSerializers(serializers.Serializer):
    latitude = serializers.CharField(required=True, allow_blank=False)
    longitude = serializers.CharField(required=True, allow_blank=False)
    height = serializers.CharField(required=True, allow_blank=False)


class LevelSerializers(serializers.Serializer):
    winter = serializers.CharField(allow_blank=True)
    summer = serializers.CharField(allow_blank=True)
    autumn = serializers.CharField(allow_blank=True)
    spring = serializers.CharField(allow_blank=True)


class ImageSerializers(serializers.Serializer):
    data = serializers.CharField()
    title = serializers.CharField()

class PerevalSerializers(serializers.Serializer):
    beauty_title = serializers.CharField(allow_blank=True)
    title = serializers.CharField(allow_blank=True)
    other_titles = serializers.CharField(max_length=300)
    connect = serializers.CharField(max_length=50, allow_blank=True)
    add_time = serializers.DateTimeField()
    user = UserSerializer(required=True)
    coords = CoordsSerializers(required=True)
    level = LevelSerializers()
    images = ImageSerializers(many=True)
