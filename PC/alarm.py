import datetime
import schedule

from connect_server import *
from connect_arduino import *
from connect_jetson import *
from utils import *


# スケジュールを読み込みアラームをセット
def load_schedule(ard_port):
    date_opt = load_date_opt()
    #print(date_opt)
    if not date_opt == None:
        set_alarm([date_opt, 'date', 0], ard_port)

    today_list = sche_list_convert(get_schedule())
    for i, j in enumerate(today_list):
        #print(i)
        set_alarm([j, 'today', i], ard_port)

    print('今日のアラームをセット完了しました')

# アラームをセット
def set_alarm(time, ard_port):
    ready_time_30 = change_minutes(time[0], -30)
    #ready_time_30 = (datetime.datetime.now() + datetime.timedelta(seconds=1)).strftime("%H:%M:%S")
    schedule.every().day.at(ready_time_30).do(pressure_reset, ard_port).tag('all', 'arduino')
    #print('    感圧センサを', ready_time_30, 'に起動します')

    ready_time_25 = change_minutes(time[0], -25)
    #ready_time_25 = (datetime.datetime.now() + datetime.timedelta(seconds=3)).strftime("%H:%M:%S")
    schedule.every().day.at(ready_time_25).do(pressure_init, ard_port).tag('all', 'arduino')

    ready_time_15 = change_minutes(time[0], -15)
    #ready_time_15 = (datetime.datetime.now() + datetime.timedelta(seconds=4)).strftime("%H:%M:%S")
    schedule.every().day.at(ready_time_15).do(pressure_init, ard_port).tag('all', 'arduino')

    ready_time_5 = change_minutes(time[0], -5)
    #ready_time_5 = (datetime.datetime.now() + datetime.timedelta(seconds=10)).strftime("%H:%M:%S")
    schedule.every().day.at(ready_time_5).do(pressure_init, ard_port).tag('all', 'arduino')


    #schedule.every().day.at(ready_time_30).do(ready_yolo).tag('all', 'jetson')
    schedule.every().day.at(ready_time_5).do(ready_yolo).tag('all', 'jetson')
    #print('    Yoloを', ready_time_5, 'に起動します')

    schedule.every().day.at(time[0]).do(wakeup_smarm, time, ard_port).tag('all', 'alarm')
    #schedule.every().day.at(ready_time_5).do(wakeup_smarm, time, ard_port).tag('all', 'alarm')

    print('    アラームを', time[0], 'に起動します')

# Smarmの起動
def wakeup_smarm(time, ard_port):
    print('起床予定時刻です', time[0])
    howto_opt = load_howto_opt()
    
    start_alarm(howto_opt)

    check_bed(ard_port)

    stop_alarm(howto_opt, time)

# アラーム起動
def start_alarm(opt):
    light_switch()

    if opt['use_sound'] == 'on':
        start_sound()
    if opt['use_air_conditioner'] == 'on':
        air_switch()
        pass
    if opt['use_tv'] == 'on':
        tv_opt = load_tv_opt()
        tv_switch_on(tv_opt[:2])
        pass
    if opt['use_out_mail'] == 'on':
        time = int(opt['out_line_time'])
        schedule.every(time).minutes.do(sent_wake_email).tag('all', 'email')
    if opt['use_servo'] == 'on':
        Servomotor()
        pass

# ベットにいるかを判定
def check_bed(ard_port):
    while True:
        get_press = pressure_get(ard_port)
        #get_press = int(input('圧力センサ\nい  る：1 / いない：0'))
        if int(get_press) == 1:
            print('圧力センサ：HIGH')
        elif int(get_press) == 0:
            print('圧力センサ：LOW')
            get_pred = predict_yolo()
            #get_pred = {'person':str(input('Yolo\nい  る：1 / いない：0'))}
            #print('get_pred', get_pred)
            if get_pred['person'] == '1':
                print('Yolo：ベットに人がいます')
                pass
            elif get_pred['person'] == '0':
                print('Yolo：ベットに人がいません')
                break

# アラーム停止
def stop_alarm(opt, time):
    if opt['use_sound'] == 'on':
        stop_sound()
    if opt['use_servo'] == 'on':
        Servomotor()
        pass
    if opt['use_tv'] == 'on':
        tv_opt = load_tv_opt()
        if tv_opt[2] == 'on':
            tv_switch_off()
            pass
    if opt['use_out_mail'] == 'on':
        schedule.clear('email')
    if opt['use_safe_mail'] == 'on':
        sent_woken_email()
    stop_yolo()

    sent_info(time)
    print('アラームを停止しました')

# 音楽の再生
def start_sound():
    sound_name = get_sound_opt()[1]
    
    pygame.mixer.init()
    pygame.mixer.music.load('./alarm_sound/'+sound_name)
    pygame.mixer.music.play(-1)

# 音楽の停止
def stop_sound():
    pygame.mixer.music.stop()