import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_api.settings')

app = Celery('weather_api', broker='amqp://localhost//')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#@app.on_after_configure.connect
#def setup_periodic_tasks(sender, **kwargs):
#    sender.add_periodic_task(30.0, 'api.tasks.update_weather_info')
