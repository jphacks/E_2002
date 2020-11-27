# Main computer
サーバ, Jetson Nano, ESP32, Arduino Nano Everyと通信を行い，起床スケジュールの読込みや，命令を送信し値の取得を行います．

# 開発環境
  - Windows10
  - Anaconda Navigator 1.10.0

### 使用言語
  - Python 3.7.9

### 必要なライブラリ
  - pygame 2.0.0
  - pyserial 3.4
  - requests 2.24.0
  - schedule 0.6.0

# 実行方法
1. smarm.pyを書き換える  


Arduino Nano Everyのポート番号を確認し，17行目のポート番号(COM10)を書き換える．
```
line 17    sen_ard = initialize("COM10", 115200)
```
2. connect_arduino.pyを書き換える  


ESP32のIPアドレスを確認し，57，63，68，73，78行目のアドレス(192.168.11.37)を書き換える．
```
line 57    requests.post('http://192.168.11.37/ledon')
```
```
line 63    requests.post('http://192.168.11.37/tvon?broad='+opt[0]+'&ch='+opt[1])
```
```
line 68    requests.post('http://192.168.11.37/tvoff')
```
```
line 73    requests.post('http://192.168.11.37/air')
```
```
line 78    requests.post('http://192.168.11.37/servo')
```
3. connect_jetson.pyを書き換える  


Jetson NanoのIPアドレスを確認し，15，22行目のアドレス(192.168.11.38:5000)を書き換える．
```
line 15    pred_result = requests.get('http://192.168.11.38:5000/api/return_result').json()
```
```
line 22    response = requests.post('http://192.168.11.38:5000/api/overwrite_state')
```
4. start_yolo.pyを書き換える  


Jetson NanoのIPアドレスを確認し，5行目のアドレス(192.168.11.38:5000)を書き換える．
```
line 5    response = requests.get('http://192.168.11.38:5000/api/start_yolo')
```
5. smarm.pyを実行する  


smarm.pyのあるフォルダ(./E_2002/PC/)に作業ディレクトリを移動し，smarm.pyを実行する<br>
`cd ./E_2002/PC/`<br>
`python smarm.py`

# 動作
1. smarm.py実行
2. Arduinoとの接続を開始
3. サーバから実行した日の起床スケジュールを読込み，保存
4. アラームをセット
5. Aruduinoに命令を送り，圧力センサの初期値をリセット，その後初期値を3回更新
6. Jetson Nanoに命令を送り，Yoloを起動
7. 起床予定時刻になると音楽を再生し，ESP32へと命令を送る
8. Arduinoから圧力センサの情報を受取る
9. 圧力センサがLOWになったとき，Jetson NanoからYoloの情報を受取る
10. Yoloがベットに人がいないと判断したとき，アラームを停止
11. 起床時刻をサーバに送信
12. 日付が変わるとArduinoとの接続を停止
13. 2へとループ
