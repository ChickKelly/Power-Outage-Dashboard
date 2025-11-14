from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class VoltageReading(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='readings')
    voltage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.station.name} - {self.voltage}V @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
