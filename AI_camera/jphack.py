from ctypes import *
import os
import cv2
import time
import darknet_jphack
import argparse
import math
import numpy as np
import datetime
import json
import subprocess

#学習されたクラス名を取得
def classname_management(altNames,data_path):
    if altNames is None:
        try:
            with open(data_path) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents, re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass
    return altNames

#クラスごとの枠を色を決める
def color_management(num_classes,class_colors,altNames):
    class_colors_own = []
    for i in range(0, num_classes):
        hue = 255*i/num_classes
        col = np.zeros((1,1,3)).astype("uint8")
        col[0][0][0] = hue
        col[0][0][1] = 128
        col[0][0][2] = 255
        cvcol = cv2.cvtColor(col, cv2.COLOR_HSV2BGR)
        col = (int(cvcol[0][0][0]), int(cvcol[0][0][1]), int(cvcol[0][0][2]))
        class_colors_own.append(col)
        class_colors[altNames[i]] = class_colors_own[i]

#YOLOによる物体検出
def image_detection(frame, network, class_names, class_colors, thresh,save_result_path,width,height):
    #物体検出のための画像の前処理
    darknet_image = darknet_jphack.make_image(width, height, 3)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet_jphack.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    #YOLOによる物体検出
    detections = darknet_jphack.detect_image(network, class_names, darknet_image, thresh=thresh)
    #検出結果枠作成
    image = darknet_jphack.draw_boxes(detections, image_resized, class_colors)
    result_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #検出結果画像保存
    pred_image = cv2.imwrite(save_result_path,result_image)
    darknet_jphack.print_detections(detections)
    return result_image, detections
                    
#カメラからの映像を取得して物体検出した結果をリアルタイムで表示
def start_process(cap,save_img_dir,save_result_dir,width,height,network,class_names,class_colors,threshold):
    start_time = time.time()
    while True:
        #state.jsonを読み込みモードでオープン
        with open('state.json', 'r') as fr:
            state_json_file = json.load(fr)
            
        #メインコンピュータから起動を求められている場合
        if state_json_file["state"] == "1":
            person_count = 0
            #カメラからの映像取得
            ret, frame = cap.read()
            #画像のパス生成
            dt_now = datetime.datetime.now()
            date = dt_now.strftime('%Y%m%d_%H%M%S%f')            
            save_result_path = str(save_result_dir + date + ".jpg")
            save_img_path = str(save_img_dir + date + ".jpg")
            #カメラからの映像を画像として保存
            cv2.imwrite(save_img_path,frame)

            #YOLOによる物体検出
            image, detections = image_detection(frame, network, class_names, class_colors, threshold,save_result_path,width,height)

            #何も検出しなかったとき
            if len(detections) == 0:
                monitor = str(0)

            #何か検出したとき
            else:
                row = np.shape(detections)[0]
                for r in range(row):
                    detection_result = detections[r][0]
                    #人を検出した場合
                    if detection_result == "person":
                        person_count += 1
                    #人以外を検出した場合
                    else:
                        pass
            if person_count >= 1:
                monitor = str(1)
            else:
                monitor = str(0)

            #経過時間
            elapsed_time = time.time() - start_time
            
            #前回の更新から1秒経過した場合
            if elapsed_time > 1:                
                jphack_dict = {"person": monitor}
                #jphack.jsonを書き込みモードでオープン
                with open('jphack.json', 'w') as fw:
                    #ベッドに人がいるかどうかの結果を書き込む
                    json.dump(jphack_dict, fw, ensure_ascii=False)
                    
                #時間をリセット
                start_time = time.time()
                
        #メインコンピュータから停止を求められている場合
        elif state_json_file["state"] == "0":
            print("finish YOLO")
            break
    
    #パソコンのパスワード
    passward = b"MIKHA\n"   
    #Jetson Nano 再起動
    subprocess.run(("sudo","-S","reboot"),input = passward , check = True)
    
#メインコンピュータからの命令によってAI Camera起動           
def ready_yolo():
    #カメラ起動
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    #YOLOの物体検出に必要なファイルのパス
    weights_path = "yolov4-tiny.weights"
    cfg_path = "cfg/yolov4-tiny.cfg"
    data_path = "cfg/coco.data"
    threshold = 0.25

    #CNNやデータのロード
    network, class_names, class_colors = darknet_jphack.load_network(
        cfg_path,
        data_path,
        weights_path,
        batch_size=1
    )

    #検出結果の画像サイズ
    width = darknet_jphack.network_width(network)
    height = darknet_jphack.network_height(network)

    #データセットの情報取得
    global metaMain, netMain, altNames
    altNames = None
    altNames = classname_management(altNames,data_path)
    num_classes = len(altNames)
    #クラスごとの枠の色決定
    color_management(num_classes,class_colors,altNames)
    
    #画像を保存するディレクトリ
    jphack_dir = "jphack"   
    ori_img_dir = "jphack/video"
    result_img_dir = "jphack/result"
    #ディレクトリがない場合にディレクトリ作成
    if not os.path.isdir(img_dir):
        os.makedirs(img_dir)
    if not os.path.isdir(ori_img_dir):
        os.makedirs(ori_img_dir)
    if not os.path.isdir(result_img_dir):
        os.makedirs(result_img_dir)
    
    #撮影日時のフォルダ作成
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y%m%d_%H%M%S')
    save_img_dir = ori_img_dir + "/" + date
    save_result_dir = result_img_dir + "/" + date
    os.makedirs(save_img_dir, exist_ok=True)
    os.makedirs(save_result_dir, exist_ok=True)
    #画像のディレクトリ作成
    save_img_dir = save_img_dir + "/"
    save_result_dir = save_result_dir + "/"

    print("--------------------------------------------------------------------------------")
    
    #カメラからの映像に対してリアルタイムで検出し、1秒おきに検出結果を書き込む
    start_process(cap,save_img_dir,save_result_dir,width,height,network,class_names,class_colors,threshold)

        

