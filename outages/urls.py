from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('history/', views.outage_history, name='history'),
    path('outage/<int:outage_id>/acknowledge/', views.acknowledge_outage, name='acknowledge_outage'),
    path('outage/<int:outage_id>/resolve/', views.resolve_outage, name='resolve_outage'),
    path('map/', views.map_view, name='map'),
]
