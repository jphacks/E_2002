import serial
import time
import requests

# ポートの指定
def initialize(port, bps):
    port = serial.Serial(port, bps)
    #print('圧力センサとの接続を開始しました')
    time.sleep(1)
    return port


# arduinoへのデータ送信
def send_command(port, byte):
    write = port.write(byte)
    data = wait_response(port)
    #pass
    return data

# arduinoから返信されるシリアル内容の表示
def wait_response(port):
    while 1:
        if port.in_waiting > 0:
            time.sleep(0.01)
            data = port.read_all().decode('utf-8')
            #print(data)
            break
    return data

# 圧力センサの初期値をリセット
def pressure_reset(port):
    pressure = {'reset':b"g", 'init': b"s", 'get':b"w"}
    init_num = send_command(port, pressure['reset'])
    #print('初期値をリセットしました')

# 圧力センサの初期値を更新
def pressure_init(port):
    pressure = {'reset':b"g", 'init': b"s", 'get':b"w"}
    init_num = send_command(port, pressure['init'])
    #print('初期値を更新しました：', init_num)

# 圧力センサからベットにいるかの判定を取得
def pressure_get(port):
    pressure = {'reset':b"g", 'init': b"s", 'get':b"w"}
    press_data = send_command(port, pressure['get'])
    #print('圧力センサの値を取得します')
    return press_data

# 圧力センサとの接続を終了
def close_port(port):
    #print('圧力センサとの接続を終了しました')
    port.close()
    pass

# ESP32と通信し，部屋の照明を点灯
def light_switch():
    requests.post('http://192.168.11.37/ledon')
    #requests.post('http://192.168.11.37/ledoff')
    print('    照明：点灯')

# ESP32と通信し，テレビの電源を入れる
def tv_switch_on(opt):
    requests.post('http://192.168.11.37/tvon?broad='+opt[0]+'&ch='+opt[1])
    print('    TV：起動')

# ESP32と通信し，テレビの電源を切る
def tv_switch_off():
    requests.post('http://192.168.11.37/tvoff')
    print('    TV：停止')

# ESP32と通信し，エアコンのスイッチを入れる
def air_switch():
    requests.post('http://192.168.11.37/air')
    print('    エアコン：起動')

# ESP32と通信し，サーボの動作させる
def Servomotor():
    requests.post('http://192.168.11.37/servo')
    print('    サーボモータ：スイッチ切り替え')
