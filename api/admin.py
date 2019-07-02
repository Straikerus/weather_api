from django.contrib import admin

from .models import Weather, ScheduledUpdate, ScheduledUpdateError, City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    pass


@admin.register(ScheduledUpdate)
class ScheduledUpdateAdmin(admin.ModelAdmin):
    pass


@admin.register(ScheduledUpdateError)
class ScheduledUpdateErrorAdmin(admin.ModelAdmin):
    pass
