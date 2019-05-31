from django.db import models


class Weather(models.Model):
    city = models.CharField('Город', max_length=200)

    # Для температуры использовал FloatField т.к. не уверен, что каждый источник
    # будет возвращать градусы в виде целого числа
    temperature = models.FloatField('Температура')
    source = models.CharField('Источник', max_length=100)
    date = models.DateTimeField('Дата и время')

    def __str__(self):
        return '{} - {} - {}'.format(self.city, self.date, self.source)
    
    class Meta:
        verbose_name = 'Погода'
        verbose_name_plural = 'Погода'
