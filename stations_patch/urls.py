from django.urls import path
from . import views

urlpatterns = [
    path('', views.stations_list, name='stations_list'),
]
