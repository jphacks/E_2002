from rest_framework import serializers # Django Rest Frameworkをインポート
from .models import Schedule, SoundFile # models.py のcouponクラスをインポート

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule # 扱う対象のモデル名を設定する
        fields = '__all__'

class SoundFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoundFile
        fields = '__all__'
