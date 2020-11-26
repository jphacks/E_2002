import datetime
import schedule
import winsound
import pygame
import time
import json

from connect_server import *
from connect_arduino import *
from connect_jetson import *
from utils import *


def load_schedule():
    opt_list = get_options()
    today_list = get_schedule()

    #print(opt_list)
    if not opt_list == None:
        set_alarm(opt_list)

    #print(today_list)
    if not today_list == []:
        for i in range(len(today_list)):
            #print(today_list[i]['start_time'])
            today_list[i] = today_list[i]['start_time']
        for i in today_list:
            #print(i)
            set_alarm(i)

    print('今日のアラームをセット完了しました')

def set_alarm(wakeup_time):
    ready_time_30 = change_minutes(wakeup_time, -30)
    #ready_time_30 = (datetime.datetime.now() + datetime.timedelta(seconds=5)).strftime("%H:%M:%S")
    #schedule.every().day.at(ready_time_30).do(pressure_reset).tag('all', 'arduino')
    #print('感圧センサを', ready_time_30, 'に起動します')
    ready_time_25 = change_minutes(wakeup_time, -25)
    #ready_time_25 = (datetime.datetime.now() + datetime.timedelta(seconds=10)).strftime("%H:%M:%S")
    #schedule.every().day.at(ready_time_25).do(pressure_init).tag('all', 'arduino')
    ready_time_15 = change_minutes(wakeup_time, -15)
    #ready_time_15 = (datetime.datetime.now() + datetime.timedelta(seconds=15)).strftime("%H:%M:%S")
    #schedule.every().day.at(ready_time_15).do(pressure_init).tag('all', 'arduino')
    ready_time_5 = change_minutes(wakeup_time, -5)
    #ready_time_5 = (datetime.datetime.now() + datetime.timedelta(seconds=20)).strftime("%H:%M:%S")
    #schedule.every().day.at(ready_time_5).do(pressure_init).tag('all', 'arduino')

    schedule.every().day.at(ready_time_5).do(ready_yolo).tag('all', 'jetson')
    #schedule.every().day.at(ready_time_30).do(ready_yolo).tag('all', 'jetson')
    print('Yoloを', ready_time_5, 'に起動します')

    schedule.every().day.at(wakeup_time).do(start_alarm).tag('all', 'alarm')
    #schedule.every().day.at(ready_time_5).do(start_alarm).tag('all', 'alarm')
    print('アラームを', wakeup_time, 'に起動します')

def start_alarm():
    now_time = datetime.datetime.now()
    print('起床予定時刻です', now_time)
    opt_schedule = requests.get('https://www.smarm-mikha.com/api/options/').json()
    #opt_schedule = {"default_alarm": "on","all_switch": "on","all_time": "07:00","holiday_switch": "on","holiday_time": "07:00","weekdays_switch": null,"weekdays_time": "07:00","day_of_the_week": 'on',"sunday_switch": 'on',"sunday_time": "07:00","monday_switch": null,"monday_time": null,"tuesday_switch": null,"tuesday_time": "07:00","wednesday_switch": null,"wednesday_time": "07:00","thursday_switch": "on","thursday_time": "07:00","friday_switch": null,"friday_time": "07:00","saturday_switch": null,"saturday_time": "07:00","use_servo": "on","use_sound": "on"}

    light_switch()

    if opt_schedule['use_sound'] == 'on':
        pygame.mixer.init()
        pygame.mixer.music.load('./alarm.mp3')
        pygame.mixer.music.play(10)
    if opt_schedule['use_servo'] == 'on':
        Servomotor()

    check_bed(now_time)

def check_bed(now_time):
    while True:
        get_press = pressure_get()

        if int(get_press) == 1:
            print('ベットにいます(圧力センサ)')
        elif int(get_press) == 0:
            stop_alarm(now_time)
            print('アラームを停止しました')
            break
            get_pred = predict_yolo()
            print('get_pred', get_pred)

            if get_pred['person'] == '1':
                print('ベットにいます(Yolo)')
                pass
            elif get_pred['person'] == '0':
                stop_alarm(now_time)
                print('アラームを停止しました')
                break

def stop_alarm(now_time):
    opt_schedule = requests.get('https://www.smarm-mikha.com/api/options/').json()
    if opt_schedule['use_sound'] == 'on':
        pygame.mixer.music.stop()
    if opt_schedule['use_servo'] == 'on':
        Servomotor()
    stop_yolo()
    sent_info(now_time)
