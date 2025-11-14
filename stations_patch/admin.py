from django.contrib import admin
from .models import Station, VoltageReading

admin.site.register(Station)
admin.site.register(VoltageReading)
