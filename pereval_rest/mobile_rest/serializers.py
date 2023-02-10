import datetime
from rest_framework import serializers
from .models import PerevalAdded, Images


class LoadDataUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, allow_blank=False)
    fam = serializers.CharField(allow_blank=True)
    name = serializers.CharField(allow_blank=True)
    otc = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)


class LoadDataCoordsSerializer(serializers.Serializer):
    latitude = serializers.CharField(required=True, allow_blank=False)
    longitude = serializers.CharField(required=True, allow_blank=False)
    height = serializers.CharField(required=True, allow_blank=False)


class LoadDataLevelSerializer(serializers.Serializer):
    winter = serializers.CharField(allow_blank=True)
    summer = serializers.CharField(allow_blank=True)
    autumn = serializers.CharField(allow_blank=True)
    spring = serializers.CharField(allow_blank=True)


class PerevalImageSerializer(serializers.Serializer):
    data = serializers.CharField()
    title = serializers.CharField()

    # ToDo переделать на работу с моделью
    # data = serializers.CharField(source='image')
    # title = serializers.CharField()
    #
    # class Meta:
    #     model = Images
    #     fields = ['title', 'data']


class LoadDataPerevalSerializer(serializers.Serializer):
    beauty_title = serializers.CharField(allow_blank=True)
    title = serializers.CharField(allow_blank=True)
    other_titles = serializers.CharField(max_length=300)
    connect = serializers.CharField(max_length=50, allow_blank=True)
    add_time = serializers.DateTimeField()
    user = LoadDataUserSerializer(required=True)
    coords = LoadDataCoordsSerializer(required=True)
    level = LoadDataLevelSerializer()
    images = PerevalImageSerializer(many=True)
    status = serializers.CharField(max_length=10, required=False)

    def create(self, validated_data):
        return PerevalTransform(**validated_data)


# ToDo сделать работу с моделью
# class PerevalAddedSerializer(serializers.ModelSerializer):
#     beauty_title = serializers.CharField(source='beautyTitle')
#     images = PerevalImageSerializer(many=True, read_only=True)
#     coords = LoadDataCoordsSerializer()
#
#     class Meta:
#         model = PerevalAdded
#         fields = ['beauty_title', 'add_data', 'images', 'coords']

class PerevalTransform:
    """
    Класс для преобразования данных из формата входящих данных в формат модели.
    Используется сериализатором.
    Служит для "развязки" сериализатора и модели.
    """

    def __init__(self, pereval: PerevalAdded = None, **kwargs) -> None:
        """
        pereval - передаем, если хотим сериализовать
        **kwargs - передаст сериализатор при десереализации
        """
        if kwargs:
            pereval_data = kwargs
        else:
            pereval_data = self._from_model(pereval)
            self.status = pereval_data['status']
        self.beauty_title = pereval_data['beauty_title']
        self.title = pereval_data['title']
        self.other_titles = pereval_data['other_titles']
        self.connect = pereval_data['connect']
        self.add_time = pereval_data['add_time']
        self.user = pereval_data['user']
        self.coords = pereval_data['coords']
        self.level = pereval_data['level']
        self.images = pereval_data['images']

    @staticmethod
    def _from_model(pereval: PerevalAdded) -> dict:
        """"
        По даннфм перевала, формирует словарь для заполнения полей этого объекта
        """
        tourist = pereval.tourist
        pereval_data = {'beauty_title': pereval.beautyTitle,
                        'title': pereval.title,
                        'other_titles': pereval.other_titles,
                        'connect': pereval.connect,
                        'add_time': pereval.add_time,
                        'user': {"email": tourist.email,
                                 "fam": tourist.last_name,
                                 "name": tourist.name,
                                 "otc": tourist.patronymic,
                                 "phone": tourist.phone, },
                        'coords': {"latitude": pereval.latitude,
                                   "longitude": pereval.longitude,
                                   "height": pereval.height},
                        'level': {"winter": pereval.winter_level,
                                  "summer": pereval.summer_level,
                                  "autumn": pereval.autumn_level,
                                  "spring": pereval.spring_level, },
                        'images': [],
                        'status': pereval.status, }
        for image in Images.objects.filter(pereval_added=pereval):
            pereval_data['images'].append(
                {'data': image.image, 'title': image.title})
        return pereval_data

    def to_model(self) -> PerevalAdded:
        new_pereval = PerevalAdded()
        new_pereval.add_data = datetime.datetime.now()

        new_pereval.user_data = self.user
        new_pereval.beautyTitle = self.beauty_title
        new_pereval.title = self.title
        new_pereval.other_titles = self.other_titles
        new_pereval.connect = self.connect
        new_pereval.add_time = self.add_time
        coords = self.coords
        new_pereval.latitude = coords['latitude']
        new_pereval.longitude = coords['longitude']
        new_pereval.height = coords['height']
        level = self.level
        new_pereval.winter_level = level['winter']
        new_pereval.spring_level = level['spring']
        new_pereval.summer_level = level['summer']
        new_pereval.autumn_level = level['autumn']

        return new_pereval
