import requests
import datetime


def get_options():
    weekday_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    opt_schedule = requests.get('https://www.smarm-mikha.com/api/options/').json()
    #opt_schedule = {"default_alarm": "on","all_switch": "on","all_time": "07:00","holiday_switch": "on","holiday_time": "07:00","weekdays_switch": null,"weekdays_time": "07:00","day_of_the_week": 'on',"sunday_switch": 'on',"sunday_time": "07:00","monday_switch": null,"monday_time": null,"tuesday_switch": null,"tuesday_time": "07:00","wednesday_switch": null,"wednesday_time": "07:00","thursday_switch": "on","thursday_time": "07:00","friday_switch": null,"friday_time": "07:00","saturday_switch": null,"saturday_time": "07:00","use_servo": "on","use_sound": "on"}
    alarm_frag = False
    if opt_schedule['default_alarm'] == 'on':
        if opt_schedule['all_switch'] == 'on':
            alarm_frag = 'all_time'
        if datetime.datetime.now().weekday() in [5, 6]:
            if opt_schedule['holiday_switch'] == 'on':
                alarm_frag = 'holiday_time'
        elif datetime.datetime.now().weekday() in [0, 1, 2, 3, 4]:
            if opt_schedule['weekdays_switch'] == 'on':
                alarm_frag = 'weekdays_time'
        if opt_schedule['day_of_the_week'] == 'on':
            if opt_schedule[weekday_list[datetime.datetime.now().weekday()] + '_switch'] == 'on':
                alarm_frag = weekday_list[datetime.datetime.now().weekday()] + '_time'
    if not alarm_frag == False:
        opt_schedule = opt_schedule[alarm_frag]
        print('設定(', alarm_frag, ')を読み込みました')
    else:
        opt_schedule = None
        print('設定を読み込みました')
    return opt_schedule

def get_schedule():
    today_schedule = requests.get('https://www.smarm-mikha.com/api/time_data/').json()
    print('スケジュールを', len(today_schedule), 'つ読み込みました')
    return today_schedule

def sent_info(now_time):
    wakeup_info = {'created_at': now_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'date': now_time.strftime('%Y-%m-%d'),
                    'end_time': datetime.datetime.now().strftime('%H:%M:%S'),
                    'id': 0,
                    'start_time': now_time.strftime('%H:%M:%S'),
                    'summary': 'Schedule'}
    requests.put('http://www.smarm-mikha.com/api/time_data/0/',
                    json.dumps(wakeup_info),
                    headers = {'Content-type': 'application/json'})
