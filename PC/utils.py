import datetime
import json
import pygame
import glob
import shutil
import os


# スケジュール情報から時間を取り出す
def sche_list_convert(sche):
    for i in range(len(sche)):
        sche[i] = sche[i]['start_time'][:-3]
    return sche

# str型からdatetime型に変換
def change_minutes(time, delta):
    time_list = time.split(':')
    time = (datetime.datetime.now().replace(hour=int(time_list[0]), minute=int(time_list[1])) + datetime.timedelta(minutes=delta)).strftime("%H:%M")
    return time

# 曜日設定オプションから時間を取り出す
def load_date_opt():
    weekday_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    week_opt = json.load(open('./server_opt/date_opt.json', 'r'))

    alarm_frag = False
    if week_opt['default_alarm'] == 'on':
        if week_opt['all_switch'] == 'on':
            alarm_frag = 'all_time'
        if datetime.datetime.now().weekday() in [5, 6]:
            if week_opt['holiday_switch'] == 'on':
                alarm_frag = 'holiday_time'
        elif datetime.datetime.now().weekday() in [0, 1, 2, 3, 4]:
            if week_opt['weekdays_switch'] == 'on':
                alarm_frag = 'weekdays_time'
        if week_opt['day_of_the_week'] == 'on':
            if week_opt[weekday_list[datetime.datetime.now().weekday()] + '_switch'] == 'on':
                alarm_frag = weekday_list[datetime.datetime.now().weekday()] + '_time'
    if not alarm_frag == False:
        week_opt = week_opt[alarm_frag]
        #print('設定(', alarm_frag, ')を読み込みました')
    else:
        week_opt = None
        #print('設定を読み込みました')
    return week_opt

# 起床方法オプションを読み込む
def load_howto_opt():
    howto_opt = json.load(open('./server_opt/howto_opt.json', 'r'))
    return howto_opt

# tvオプションを読み込む
def load_tv_opt():
    tv_opt = json.load(open('./server_opt/tv_opt.json', 'r'))
    mode = tv_opt['bs_or_digital']
    ch = tv_opt['select_channel'][0]
    toggle = tv_opt['tv_toggle_switch']
    return mode, ch, toggle

# 音声ファイルに重複がないか検索
def search_sound_file(name):
    file = glob.glob('./alarm_sound/*')
    file_list = [i.split('\\')[-1] for i in file]

    if name in file_list:
         return False
    else:
        return True

# 音声フォルダをリセットする
def reset_sound_file():
    file = glob.glob('./alarm_sound/*')
    print(file)
    shutil.rmtree('./alarm_sound')
    os.mkdir('./alarm_sound')

# 設定したアラームをすべて削除する
def reset_schedule():
    schedule.clear('all')