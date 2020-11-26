import requests
import time
import subprocess


def ready_yolo():
	start_yolo = subprocess.Popen(['python', 'start_yolo.py'],shell=False)
	time.sleep(5)
	start_yolo.kill()

def predict_yolo():
    pred_result = requests.get('http://192.168.11.35:5000/api/return_result').json()
    print(pred_result)
    return pred_result

def stop_yolo():
    response = requests.post('http://192.168.11.35:5000/api/overwrite_state')