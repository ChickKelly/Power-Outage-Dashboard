from django.shortcuts import render, redirect
from .models import Station, VoltageReading

def stations_list(request):
    stations = Station.objects.all()
    return render(request, 'stations_patch/stations_list.html', {'stations': stations})
