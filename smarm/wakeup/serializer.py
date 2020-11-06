from rest_framework import serializers # Django Rest Frameworkをインポート
from .models import Schedule # models.py のcouponクラスをインポート

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule # 扱う対象のモデル名を設定する
        fields = '__all__'
