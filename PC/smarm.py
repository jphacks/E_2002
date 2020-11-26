import datetime
import time

from connect_server import *
from connect_arduino import *
from connect_jetson import *
from alarm import *
from utils import *


def main():
    while True:
        time.sleep(1)
        today = datetime.date.today()
        print('日付を更新します：', today)
        
        sen_ard = initialize("COM10", 115200)
        #sen_ard = 0

        get_all_opt()
        load_sound(get_sound_opt())
        load_schedule(sen_ard)
        
        while today == datetime.date.today():
            schedule.run_pending()
            try:
                time.sleep(1)
                print('\n')
            except KeyboardInterrupt:
                break
            
        close_port(sen_ard)
        reset_schedule()

if __name__ == "__main__":
    main()