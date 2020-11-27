# SMARM.com
Djangoフレームワークで作成したWEBアプリケーションです。  
メインPCやESP32とREST APIを使用して通信を行い、データの送伝達を行っています。  
また、ローカル環境だけではなく、さくらVPSを利用して，本番環境としての実装も行っています。  

# WEBアプリケーション説明
## ページURL
https://jphack-smarm.com/  
## ページ毎の説明
### 1.TOPページ
起床時間のグラフを見るためのページです。
使用者のニーズに対応できるように
横軸をDAY，WEEK，MONTHの3つから選択できるようにしました。
加えて、朝起きる時間にムラがある方のために、目標時間との差を表示する機能も追加しました。

### 2.SCHEDULEページ
目覚ましを掛ける時間を設定するためのページです。
カレンダーの部分は下記のサイトを参考にさせていただきました。  

Djangoでカレンダーを作るシリーズ  
https://blog.narito.ninja/detail/11  
github  
https://github.com/naritotakizawa/django-simple-calendar  

こちらの方のコードをベースにsmarmに適した形になるように書き換えています。

### 3.HOWTOページ
予定がない場合に目覚ましを起動するかや，起床方法について設定できるページです。
デバイスへのデータ転送のために送受信用のAPIを作成しています。

#### データ送受信用のAPIについて
データ送受信用のAPI
- その日のスケジュールを送信するAPI  
"https://jphack-smarm.com/api/time_data/"  
- HOWTOページの設定データを送信するAPI  
"https://jphack-smarm.com/api/how_to_options/"
- HOWTOページに設定された目覚まし用の音声ファイルのURLを送信するAPI  
"https://jphack-smarm.com/api/melody/"
- HOWTOページに設定されたエアコンに命令するための配列を送信するAPI  
"https://jphack-smarm.com/api/air_conditioner_options/"
- HOWTOページに設定されたメールアドレスに遅刻時のメール送信を行うAPI  
"https://jphack-smarm.com/api/send_out_mail/"
- HOWTOページに設定されたメールアドレスに起床時のメール送信を行うAPI  
"https://jphack-smarm.com/api/send_safe_mail/"

##### ※メールの送信に関しては、悪用の危険があるため，実際には送信しない設定にしています。本番運用する際には、SMTPサーバーを利用します。

## 今後の展望
* メールだけでなく、LINE APIを使用したLINEへの通知機能
* 各デバイス毎のID，パスワードを設定し，1つのベッド毎に管理し対応できるようにする。
* JavaやKotlin,swiftを使用して、スマホ用のレイアウトを作成する。

## 注力したことと意気込み
* 初めて見た人でも使いやすいレイアウト，機能を心掛けました。
* Djangoを使用したことも、サーバー構築したことも今回が初めてでしたが、今の自分の精一杯の出来だと自負しています。

## 開発技術
### フレームワーク・ライブラリ・モジュール
#### フレームワーク  
* Django  
#### ライブラリ 
* requirements.txtに記載
#### RDB  
* PostgerSQL(githubはsqlite版をupload)  
#### 本番環境    
* さくらVPS  
* nginx  
* gunicorn  

#### 言語
* Python
* JavaScript

### 独自技術
#### ハッカソンで開発した独自機能・技術
* webアプリから様々な方法で目覚ましを設定できる。
* webアプリからデバイスへのデータの送受信を自動で行ってくれる。
* さくらVPSを用いて、ローカル環境でなくとも、目覚ましを設定できる。
* 起床時または寝坊時にメールを送信してくれる。

#### 特に力を入れた部分  
DBからグラフに可視化するためのデータの受け渡し部分  
smarm/wakeup/views.py  
OPTIONページの，スイッチ切り替えによる特定ボタンの無効化部分  
smarm/wakeup/templates/wakeup/howto.html  
