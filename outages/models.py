# outages/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# --------------------------
# Custom User Model
# --------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('repair_team', 'Repair Team'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='repair_team')

    def __str__(self):
        return f"{self.username} ({self.role})"


# --------------------------
# Community Model
# --------------------------
class Community(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    power_status = models.BooleanField(default=True)
    voltage = models.FloatField(default=0)  # Current voltage

    def __str__(self):
        return self.name


# --------------------------
# Voltage Reading Model
# --------------------------
class VoltageReading(models.Model):
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='readings'
    )
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.community.name}: {self.value}V at {self.timestamp}"


# --------------------------
# Outage Model
# --------------------------
class Outage(models.Model):
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='outages'
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Acknowledgment
    is_acknowledged = models.BooleanField(default=False)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='acknowledged_outages'
    )

    # Resolution
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='resolved_outages'
    )

    def __str__(self):
        status = "Resolved" if self.is_resolved else "Active"
        return f"{self.community.name} outage ({status})"
