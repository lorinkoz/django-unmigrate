from django.db import models


class MyModel(models.Model):

    name = models.CharField(max_length=30, blank=True)
    tz_created = models.DateTimeField(auto_now_add=True)
