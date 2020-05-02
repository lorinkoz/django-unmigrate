from django.db import models


class MyModel(models.Model):

    name = models.CharField(max_length=30, blank=True)
    tz_created = models.DateTimeField(auto_now_add=True)

    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
