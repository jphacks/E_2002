# Generated by Django 2.2 on 2020-11-01 15:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wakeup', '0002_auto_20201101_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Alarm'),
        ),
    ]
