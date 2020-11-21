import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Schedule(models.Model):
    """スケジュール"""
    summary = models.CharField('Schedule', max_length=50)
    start_time = models.TimeField('Alarm', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('WakeUp', blank=True, null=True)
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.summary

class SoundFile(models.Model):
    #title = models.CharField('Schedule', max_length=30)
    file = models.FileField(
    '音声ファイル',
    validators=[FileExtensionValidator(allowed_extensions=['mp3',''])])

    def __str__(self):
        return self.file.url
