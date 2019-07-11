from django.utils import timezone
from django.db import models

from core.db.manager import CustomManager


class City(models.Model):
    name = models.CharField('Название', max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Weather(models.Model):
    objects = CustomManager()
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)

    # Для температуры использовал FloatField т.к. не уверен, что каждый источник
    # будет возвращать градусы в виде целого числа
    temperature = models.FloatField('Температура')
    source = models.CharField('Источник', max_length=100)
    datetime = models.DateTimeField('Дата и время', auto_now_add=True)

    def __str__(self):
        return '{} - {} - {}'.format(
            self.city,
            timezone.localtime(self.datetime),
            self.source
        )
    
    class Meta:
        verbose_name = 'Погода'
        verbose_name_plural = 'Погода'


class ScheduledUpdate(models.Model):
    STATUS_CHOICES = [
        (0, 'Успешно'),
        (1, 'Имеются ошибки при обновлении')
    ]
    datetime = models.DateTimeField(
        'Дата обновления',
        auto_now_add=True
    )
    status = models.SmallIntegerField('Статус обновления', choices=STATUS_CHOICES)

    def __str__(self):
        return '{} {}'.format(timezone.localtime(self.datetime), self.get_status_display())
    
    class Meta:
        verbose_name = 'Плановое обновление'
        verbose_name_plural = 'Плановые обновления'


class ScheduledUpdateError(models.Model):
    scheduled_update = models.ForeignKey(
        ScheduledUpdate,
        verbose_name='Плановое обновление',
        on_delete=models.CASCADE
    )
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    source = models.CharField('Название источника', max_length=100)
    error = models.TextField('Текст ошибки')

    def __str__(self):
        return '{} {}'.format(self.source, self.city)
    
    class Meta:
        verbose_name = 'Ошибка планового обновления'
        verbose_name_plural = 'Ошибки плановых обновлений'
