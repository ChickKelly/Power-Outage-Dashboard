from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Community, Outage

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)
@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'power_status', 'latitude', 'longitude')
    list_filter = ('power_status',)
    search_fields = ('name',)

@admin.register(Outage)
class OutageAdmin(admin.ModelAdmin):
    list_display = ('community', 'start_time', 'end_time', 'is_resolved', 'resolved_by')
    list_filter = ('is_resolved', 'community')
    search_fields = ('community__name',)
