from django.db import models
from django.contrib.auth.models import User
import uuid

class Driver(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drivers', null=True, blank=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_delivery', 'On Delivery'),
    ]
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_online = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Cargo(models.Model):
    name = models.CharField(max_length=255)
    driver = models.ForeignKey(Driver, related_name='cargos', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DriverLocationHistory(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='location_history')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.driver.name} at {self.timestamp}"
