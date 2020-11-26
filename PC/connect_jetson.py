import requests
import time
import subprocess


# Jetson Nanoと通信し，Yoloを起動
def ready_yolo():
    start_yolo = subprocess.Popen(['python', './subprocess_file/start_yolo.py'],shell=False)
    print('Yoloを起動します')
    time.sleep(1)
    start_yolo.kill()

# Jetson Nanoと通信し，ベットに人がいるかの判定を取得
def predict_yolo():
    pred_result = requests.get('http://192.168.11.38:5000/api/return_result').json()
    #print('Yoloの結果を表示します')
    #pred_result = 1
    return pred_result

# Jetson Nanoと通信し，Yoloを停止，Jetson Nanoの再起動
def stop_yolo():
    response = requests.post('http://192.168.11.38:5000/api/overwrite_state')
    #print('    Yoloを停止しました')
    #pass