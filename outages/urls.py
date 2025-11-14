from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Communities
    path('community_list/', views.community_list, name='community_list'),
    path('community_list/edit/<int:pk>/', views.edit_community, name='edit_community'),
    path('community_list/delete/<int:pk>/', views.delete_community, name='delete_community'),
    
    # Outages
    path('outages/', views.outages_list, name='outages'),
    path('acknowledge/<int:outage_id>/', views.acknowledge_outage, name='acknowledge_outage'),
    path('resolve/<int:outage_id>/', views.resolve_outage, name='resolve_outage'),

    # Map & History
    path('map/', views.map_view, name='map_view'),
    path('history/', views.history, name='history'),

    # Add city
    path('add_city/', views.add_city, name='add_city'),
]
