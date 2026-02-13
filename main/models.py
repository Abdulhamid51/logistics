from django.db import models
import uuid

class Driver(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
