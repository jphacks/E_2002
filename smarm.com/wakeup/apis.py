from .models import Schedule, SoundFile
from rest_framework import viewsets, routers
from .serializer import ScheduleSerializer, SoundFileSerializer
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import json
from datetime import datetime as dt

class ScheduleViewSet(viewsets.ModelViewSet):
    d_today = datetime.date.today()
    queryset = Schedule.objects.filter(date=d_today) # 全てのデータを取得
    serializer_class = ScheduleSerializer



class SoundFileViewSet(viewsets.ModelViewSet):
    json_open = open('wakeup/json/how_to_options.json', 'r')
    json_load = json.load(json_open)
    queryset = SoundFile.objects.filter(id=int(json_load['select_melody_id']))
    #print(SoundFile.objects.all()) # 全てのデータを取得
    serializer_class = SoundFileSerializer

router = routers.DefaultRouter()
router.register(r'time_data', ScheduleViewSet)
router.register(r'melody', SoundFileViewSet)

def how_to_options(request):
    json_howto_open = open('wakeup/json/how_to_options.json', 'r')
    json_howto_load = json.load(json_howto_open)
    json_date_open = open('wakeup/json/date_options.json', 'r')
    json_date_load = json.load(json_date_open)
    json_tv_open = open('wakeup/json/tv_options.json', 'r')
    json_tv_load = json.load(json_tv_open)
    #json形式の文字列を生成
    json_load = {"date":json_date_load, "howto":json_howto_load, "tv":json_tv_load }
    json_str = json.dumps(json_load, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)

def send_safe_mail(request):
    json_open = open('wakeup/json/mail_options.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)
    #json形式の文字列を生成
    name = json_load["safe_mail_from"]
    email = json_load["safe_mail_to"]
    subject = json_load["safe_mail_subject"]
    message_main = json_load["safe_mail_message"]
    if subject== "":
        subject="{}の起床報告".format(name)
    if message_main== "":
        tdatetime = dt.now()
        tstr = tdatetime.strftime('%H時%M分')
        message_main = "{0}は{1}に起きました。".format(name,tstr)
    message = "送信者名：{0}\nメッセージ：{1}".format(name,message_main)
    from_email = 'mikha0928@gmail.com'
    to_list = json_load["safe_mail_to"].split()
    try:
        send_mail(subject, message, from_email, to_list)
        return HttpResponse("OK")
    except:
        return HttpResponse("Fail send mail")

def send_out_mail(request):
    json_open = open('wakeup/json/mail_options.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)
    #json形式の文字列を生成
    name = json_load["out_mail_from"]
    email = json_load["out_mail_to"]
    subject = json_load["out_mail_subject"]
    message_main = json_load["out_mail_message"]
    if subject== "":
        subject="{}がまだ起きていません".format(name)
    if message_main== "":
        message_main = "{}がまだ起きていません。起こしてあげてください。".format(name)
    message = "送信者名：{0}\nメッセージ：{1}".format(name,message_main)
    from_email = 'mikha0928@gmail.com'
    to_list = json_load["out_mail_to"].split()

    try:
        send_mail(subject, message, from_email, to_list)
        return HttpResponse("OK")
    except:
        return HttpResponse("Fail send mail")

def air_conditioner_options(request):
    json_open = open('wakeup/json/air_conditioner_options.json', 'r')
    json_load = json.load(json_open)
    select_temp_s = 'on_' + json_load["hot_or_cool"] + '_' + json_load["set_temp"]
    json_database_open = open('wakeup/json/air_conditioner_commands.json', 'r')
    json_database_load = json.load(json_database_open)
    json_data = json_database_load[select_temp_s]
    #json形式の文字列を生成
    json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)
