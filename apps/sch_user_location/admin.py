from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'school', 'sta_dist_one', 'sta_dist_two', 'latitude', 'longitude', 'create_time')
    list_per_page = 50