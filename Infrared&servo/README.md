# Esp32 Server(Infrared&Servo motor)
ESP32を使って赤外線LEDやサーボモータを動かす部分の説明です．<br>
PCからWi-Fiを経由して送られた命令を元に，部屋の照明・TV・エアコン・サーボモータを動かすことができます．<br>
<img src="https://user-images.githubusercontent.com/73453598/100401204-2349c280-309c-11eb-8118-76362f712df7.jpg" width="300px">
<!-- 装置全体の画像を貼る予定 -->

## Demo
実際に家電やサーボモータを動かした時の様子です．<br>
<img src="https://user-images.githubusercontent.com/73453598/100400848-2bedc900-309b-11eb-8c3d-a955b91ceb5e.gif" width="600px">

## Usage
**※使用する前に赤外線リモコンの送信コードを調べておく必要があります．<br>
(使いたい赤外線の情報をサーバに保存するような機能も追加したかったですが，時間が足りませんでした(´・ω・｀))**<br>
**↓リンク先のコードを使用することで赤外線の読み取りができます．**<br>
<https://github.com/crankyoldgit/IRremoteESP8266/blob/master/examples/IRrecvDumpV3/IRrecvDumpV3.ino>

curlコマンドを使える環境があれば以下のコマンドを打つことで簡単に試すことができます．<br>
broadはdigitalとbsの二択でチャンネルは1~12chまで対応しています．<br>
エアコンのON/OFFに必要な配列はサーバから自動的に取得します．<br>
サーボモータの動作に関しては，命令を送るたびにON/OFFが交互に切り替わるようになっています．<br>

```
curl <IPアドレス>/ledon
curl <IPアドレス>/ledoff
curl <IPアドレス>/tvon?broad=broad\&ch=1
curl <IPアドレス>/tvoff
curl <IPアドレス>/air
curl <IPアドレス>/servo
```

## Setup
セットアップするのに特別な手順は必要ありません．<br>
Arduino IDEを自身のPCにインストールして，ESP32にプログラムを書き込めば動きます．<br>

## Schematic
使用した部品は以下の通りで，回路図に示すように配線を行いました．
- sg90(マイクロサーボモータ)
- Mg996r(サーボモータ)
- VS1838B(赤外線受光モジュール)
- 赤外線LED×3
- 抵抗(10Ω×2, 1kΩ×1)
- 2N2222(トランジスタ)

![esp32_schematic](https://user-images.githubusercontent.com/73453598/100362952-6b86c780-303f-11eb-844b-4452e7f9814c.png)<!-- 回路図を載せる -->

## Dependency

### 開発言語
- Arduino言語

### 開発環境
- Arduino IDE ver1.8.13

### 使用したライブラリ
- Arduino_JSON ver0.1.0
- ESP32Servo ver0.9.0
- IRremoteESP8266 ver2.7.12
