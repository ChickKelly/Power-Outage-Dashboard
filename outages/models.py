from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('repair_team', 'Repair Team'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='repair_team')

class Community(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    power_status = models.BooleanField(default=True)  # True for ON, False for OFF
    voltage = models.FloatField(default=0.0)   # ✅ add voltage
    last_update = models.DateTimeField(null=True, blank=True)  # ✅ last update timestamp


    def __str__(self):
        return self.name

class Outage(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_outages')
    is_acknowledged = models.BooleanField(default=False)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='acknowledged_outages')
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Outage in {self.community.name} at {self.start_time}"
# outages/models.py
from django.db import models

class City(models.Model):
    id = models.AutoField(primary_key=True)  # optional, Django already has this
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.id})"
