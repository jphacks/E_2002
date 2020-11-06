import datetime

def change_minutes(time_str, delta):
    time_list = time_str.split(':')
    time_str = (datetime.datetime.now().replace(hour=int(time_list[0]), minute=int(time_list[1])) + datetime.timedelta(minutes=delta)).strftime("%H:%M")
    return time_str