from .models import Schedule
from rest_framework import viewsets, routers
from .serializer import ScheduleSerializer
import datetime
from django.shortcuts import render
from django.http import HttpResponse
import json

class ScheduleViewSet(viewsets.ModelViewSet):
    d_today = datetime.date.today()
    print(d_today)
    queryset = Schedule.objects.filter(date=d_today) # 全てのデータを取得
    serializer_class = ScheduleSerializer

router = routers.DefaultRouter()
router.register(r'time_data', ScheduleViewSet)

def options(request):
    json_open = open('wakeup/how_to_options.json', 'r')
    json_load = json.load(json_open)

    #json形式の文字列を生成
    json_str = json.dumps(json_load, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)
