import requests
import datetime
import json
import shutil

from utils import search_sound_file


# サーバから情報を取得し，保存
def get_all_opt():
    all_opt = requests.get('https://jphack-smarm.com/api/how_to_options/').json()
    #all_opt = {'date':{'default_alarm': 'on', 'all_switch': 'on', 'all_time': '07:00', 'holiday_switch': 'on', 'holiday_time': '07:00', 'weekdays_switch': None, 'weekdays_time': '07:00', 'day_of_the_week': None, 'sunday_switch': None, 'sunday_time': '07:00', 'monday_switch': None, 'monday_time': None, 'tuesday_switch': None, 'tuesday_time': '07:00', 'wednesday_switch': None, 'wednesday_time': '07:00', 'thursday_switch': 'on', 'thursday_time': '07:00', 'friday_switch': None, 'friday_time': '07:00', 'saturday_switch': None, 'saturday_time': '07:00'},
    #          'howto':{"use_servo": "on","use_sound": "on", "use_tv": "on", "use_air": "on"},
    #          'tv':{"tv_toggle_switch":"off", "bs_or_digital":"BS", "select_channel":"1ch"}
    #          }

    with open('./server_opt/date_opt.json', 'w') as f:
        json.dump(all_opt['date'], f, indent=4)
        
    with open('./server_opt/howto_opt.json', 'w') as f:
        json.dump(all_opt['howto'], f, indent=4)
        
    with open('./server_opt/tv_opt.json', 'w') as f:
        json.dump(all_opt['tv'], f, indent=4)

    print('本日の起床スケジュールを取得しました')

# 今日の予定を読み込む
def get_schedule():
    today_schedule = requests.get('https://jphack-smarm.com/api/time_data/').json()
    if today_schedule == []:
        #print('\n今日の予定はありませんでした')
        pass
    elif len(today_schedule[0]) > 0:
        #print('\n今日の予定を', len(today_schedule), 'つ読み込みました')
        pass

    return today_schedule

# 音楽の設定を読み込む
def get_sound_opt():
    response = requests.get('https://jphack-smarm.com/api/melody/').json()
    if response == []:
        response = 0
        file_name = 'sound.mp3'
    else:
        response = response[0]
        file_name = response['file'].split('/')[-1]

    return response, file_name

# 音楽をダウンロード
def load_sound(opt):
    if not opt[0] == 0:
        sound_data = requests.get(opt[0]['file'], stream=True)
        if sound_data.status_code == 200:
            if search_sound_file(opt[1]):
                with open('./alarm_sound/'+opt[1], 'wb') as f:
                    sound_data.raw.decode_content = True
                    shutil.copyfileobj(sound_data.raw, f)

# 起床情報をサーバに送信
def sent_info(time):
    if time[1] == 'date':
        wakeup_info = {'summary': 'date_opt',
                        'start_time': time[0]+':00',
                        'end_time': datetime.datetime.now().strftime('%H:%M:%S'),
                        'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                        'created_at': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}

        response = requests.post('https://jphack-smarm.com/api/time_data/',
                                    json.dumps(wakeup_info),
                                    headers = {'Content-type': 'application/json'})
    elif time[1] == 'today':
        wakeup_info = requests.get('https://jphack-smarm.com/api/time_data/').json()[time[2]]
        wakeup_info['end_time'] = datetime.datetime.now().strftime('%H:%M:%S')

        response = requests.put('https://jphack-smarm.com/api/time_data/'+str(wakeup_info['id'])+'/',
                                    json.dumps(wakeup_info),
                                    headers = {'Content-type': 'application/json'})

# 起床していないメールを送信
def sent_wake_email():
    response = requests.get('https://jphack-smarm.com/api/melody/').json()
    #pass

# 起床したメールを送信
def sent_woken_email():
    response = requests.get('https://jphack-smarm.com/api/melody/').json()
    #pass