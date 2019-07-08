import datetime

from celery.decorators import periodic_task

from .models import City, ScheduledUpdateError, ScheduledUpdate
from weather_api.celery import app
from .utils import update_cities


@periodic_task(run_every=60.0)
def update_weather_info():
    cities_list = City.objects.values_list('name', flat=True)
    error_logs = update_cities(cities_list)
    scheduled_update_object = ScheduledUpdate(status=0)
    if len(error_logs) > 0:
        scheduled_update_object.status = 1
        scheduled_update_object.save()
        error_objects = []
        for city, errors_dict in error_logs.items():
            for source, error in errors_dict.items():
                error_objects.append(
                    ScheduledUpdateError(
                        scheduled_update=scheduled_update_object,
                        city_id=City.objects.only('id').get(name=city).id,
                        source=source,
                        error=error
                    )
                )
        ScheduledUpdateError.objects.bulk_create(error_objects)
    else:
        scheduled_update_object.save()
