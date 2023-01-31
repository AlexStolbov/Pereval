from django.db import models


class Tourist(models.Model):
    name = models.CharField(max_length=100)
