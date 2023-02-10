from enum import Enum
from django.db import models


class Tourist(models.Model):
    """
    Туристы, присылающие данные о прохождении перевалов
    "user": {
        "email": "user@email.tld",
        "phone": "79031234567",
        "fam": "Пупкин",
        "name": "Василий",
        "otc": "Иванович"
    },
    """
    email = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)


class PerevalAreas(models.Model):
    """
    Справочник регионов перевалов.
    """
    parent = models.ForeignKey(to='self',
                               name='parent',
                               null=True,
                               on_delete=models.SET_NULL)
    title = models.CharField(max_length=150)


class PerevalAdded(models.Model):
    """
    Данные о прохождении перевалов, присланные туристами.
    """
    # Сырые данные, переданные туристом.
    row_data = models.JSONField()
    # Дата и время загрузки в базу.
    add_data = models.DateTimeField()
    # временно хранит данные туриста
    user_data = {}
    # по email подбирается существующий, или создается новый
    tourist = models.ForeignKey(Tourist, null=True, on_delete=models.SET_NULL)
    beautyTitle = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=300)
    connect = models.CharField(max_length=50)
    add_time = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()
    winter_level = models.CharField(max_length=5)
    spring_level = models.CharField(max_length=5)
    summer_level = models.CharField(max_length=5)
    autumn_level = models.CharField(max_length=5)
    # Заполняется после утверждения маршрута
    pereval_areas = models.ForeignKey(PerevalAreas,
                                      null=True,
                                      on_delete=models.SET_NULL)
    # Moderation status
    status = models.CharField(max_length=10)

    class ModerationStatus(Enum):
        New = 'new'
        Pending = 'pending'  # модератор взял в работу;
        Accepted = 'accepted'  # модерация прошла успешно;
        Rejected = 'rejected'  # модерация прошла, информация не принята.


class Images(models.Model):
    pereval_added = models.ForeignKey(PerevalAdded,
                                      related_name='images',
                                      on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='')
    image = models.BinaryField()

    class Meta:
        ordering = ['title']
