# Generated by Django 2.2.1 on 2019-07-08 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20190708_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledupdate',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления'),
        ),
    ]