from connect_server import *
from connect_arduino import *
from connect_jetson import *
from alarm import *
from utils import *
import datetime
import time


def main():
    while True:
        time.sleep(1)
        today = datetime.date.today()
        load_schedule()
        
        while today == datetime.date.today():
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    main()