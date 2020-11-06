# SMARM

[![IMAGE SMARM](https://jphacks.com/wp-content/uploads/2020/09/JPHACKS2020_ogp.jpg)](https://www.youtube.com/watch?v=G5rULR53uMk)

## 製品概要
目覚まし×Tech
### 背景(製品開発のきっかけ、課題等）
私たちは目覚ましで起きられない、出張でいつもより早く起きなければならない、そんな方々に確実な起床を促すシステムを提案します。
このシステムは昨今のコロナウイルスの影響により在宅ワークをしていた方がコロナウイルス収束に伴って通常勤務に戻った際に生活リズムを取り戻す手段として大いに役立ちます。
AIを活用して人間の起床を管理するプログラムと起床を促すデバイスを開発して連携し、あらかじめ設定した時間になっても人が起床していないとAIが判断した場合に起床デバイスに命令を出して起床させるシステムを開発しました。このシステムを導入すれば寝坊による遅刻回避は間違いなく、皆様に快適な朝の時間を過ごしていただけることを確約します！

### 製品説明（具体的な製品の説明）
目覚まし機能を有したIotベッドです。
#### 使い方
1.「smarm」 https://www.smarm-mikha.com/ にアクセスして、[Schedule]や[HOW TO WAKEUP]ページから目覚ましを掛ける時間や方法を設定します。
時間の設定方法は様々で、
* 1日毎に予定と合わせて設定
![Smart Alarm - Google Chrome 2020-11-06 14-39-58 (3)](https://user-images.githubusercontent.com/73453598/98354102-9b0b6b00-2063-11eb-9a10-a9e14fe3c861.gif)

* 複数の予定を一度に設定
![Smart Alarm - Google Chrome 2020-11-06 14-41-29 (3)](https://user-images.githubusercontent.com/73453598/98354194-ba09fd00-2063-11eb-9362-0ba556e25528.gif)

* 予定を設定していない日に目覚ましを掛けるかどうかの設定
![Smart Alarm - Google Chrome 2020-11-06 14-44-25 (3)](https://user-images.githubusercontent.com/73453598/98354458-1705b300-2064-11eb-97bf-588dac15cdb8.gif)

このように使用者のニーズに合わせた時間や目覚まし方法の設定が可能です。

2. 設定した時間と方法で目覚ましを開始します。
ベッドから出るまで決して止まりません。

3. smarmトップページから，自分の起床時間の推移をグラフで確認できます。
起床時間だけでなく、起床時間と目標時間との差も見ることができるため，目覚まし開始から何分で起きれているかを管理することも可能です。

![Smart Alarm - Google Chrome 2020-11-06 19-56-29](https://user-images.githubusercontent.com/73453598/98358656-6222c480-206a-11eb-836a-5fbdfb46e8d5.gif)




#### 構成
本サービスのデバイス構成はこちらの図のようになっています。
![構成図1](https://user-images.githubusercontent.com/73453598/98344625-dbb0b780-2056-11eb-8935-f7b26ac390a2.png)

システムの主な流れは，
1. 毎日0時頃にwebアプリケーションから時間や起床方法情報を取得。

2. 目覚まし予定があれば、目覚まし5分前にカメラをセットアップ開始(時間がかかるため)。
3. 目覚まし直前に赤外線モジュールで部屋の明かりをつける。
4. 時間になると、アラーム音とサーボモータによる目覚ましを開始。
5. カメラと圧力センサから人を監視。数秒ごとに情報を取得し、カメラと圧力センサ両方から人がいない判定が返ってくれば終了。
6．終了の際に，起きた時間をwebアプリケーションに送信。
7. 次のスケジュールがあればその時間まで待機し→2.へ。
   なければ→1．へ

となっています。

### 特長
#### 1. 特長1
* 早起きの習慣化を目指したシステム設計
本サービスは早起きの習慣化を目標に、
毎日、自動で目覚ましをセット、起動、終了を行うことができます。

#### 2. 特長2
* アラームだけでは起きられない人のための目覚まし
本サービスが対象としている、朝起きられない人の中には、「アラームが鳴り続けても寝続ける人」も多くいると思います。
そんな方のために、アラーム以外のアプローチであなたの起床を促します。　
　
![00116 (1)](https://user-images.githubusercontent.com/73453598/98352799-d9a02600-2061-11eb-87b3-33bf0222de31.gif)

#### 3. 特長3
* 使いやすさと見やすさを重視したwebアプリケーション
利用者が早起きのモチベーションを維持するため，
ストレスの少ない柔軟な時間設定と、起床時間の推移が見やすくなるよう心掛けて設計しました。

### 解決出来ること
* 朝が弱い人でも起きられるようになる。
* 目覚ましをwebアプリから容易にセットでき、目覚ましのつけ忘れが減少する。
* 起きた時間をグラフで見れるため、早起きの習慣化を実感できる。

### 今後の展望
* 通信をwifiもしくはBlurtoothで行い、PCの部分をjetsonnanoやRaspberry Piに変えることでより小型化を目指し，ベッドへの組み込みを容易にする。
* アラームに音楽を設定や、テレビを大音量で流すなど、目覚ましのアプローチを増やす。
* サーモカメラを用いて独自の学習モデルを開発し用いることでカメラの人物検出の精度を向上させる。
* ログイン機能等をつけて1つのベッド毎に対応できるようにする。

### 注力したこと（こだわり等）
* すべてのデバイスをベッドに組み込めるような構成にしました。
* 私たちが所属しているロボット・知能システム学研究室の強みを活かし、カメラによる物体検出の手法には研究でも使用しているYolov4を選びました。

![detection_demo_result (2)](https://user-images.githubusercontent.com/73453598/98355081-0275ea80-2065-11eb-8d20-70f21f6649ca.gif)

* 絶対に起こすという意志の下、あえて目覚ましを止めるスイッチをどこにもつけていません。


## 開発技術
### 活用した技術
#### API・データ
* AWS
* COCOデータセット

#### フレームワーク・ライブラリ・モジュール
* Django
* Darknet
* 赤外線モジュール
* 圧力センサ
* サーボモータ
* Python
* JavaScript
* C++
* Chart.js

#### デバイス
* Arduino
* jetson nano
* PC

### 独自技術
#### ハッカソンで開発した独自機能・技術
* webアプリから様々な方法で目覚ましを設定できる。
* webアプリからデバイスへのデータの送受信を自動で行ってくれるようにした。
* AWSを用いて、ローカル環境でなくとも、目覚ましを設定できるようにした。
* カメラによる物体検出と，ベッドの足につけた圧力センサによる荷重検出により、ベッドからでるまで止まらない目覚ましを開発した。
* 赤外線モジュールを用いて自動で部屋の電気をオンにできるようにした。
* サーボモータを用いて物理的に目覚めを促す機構を開発した。

* 特に力を入れた部分をファイルリンク、またはcommit_idを記載してください。

#### 製品に取り入れた研究内容（データ・ソフトウェアなど）（※アカデミック部門の場合のみ提出必須）
Yolo v4 
