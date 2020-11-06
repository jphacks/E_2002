from ctypes import *
import random
import os
import cv2
import time
import darknet_jphack
import argparse
from threading import Thread, enumerate
from queue import Queue
import math
import gc
import traceback
import numpy as np
import glob
import collections
import shutil
import datetime
from multiprocessing import Value, Array, Process
import json

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

def image_detection(image_path, network, class_names, class_colors, thresh,save_result_path,width,height):
    darknet_image = darknet_jphack.make_image(width, height, 3)
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet_jphack.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet_jphack.detect_image(network, class_names, darknet_image, thresh=thresh)

    image = darknet_jphack.draw_boxes(detections, image_resized, class_colors)
    result_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pred_image = cv2.imwrite(save_result_path,result_image)
    darknet_jphack.print_detections(detections)
    return result_image, detections
    
def yolo_process(img_path,save_result_path):
    image, detections = image_detection(img_path, network, class_names, class_colors, args.thresh,save_result_path)
            
    if len(detections) == 0:
        monitor = str(0)

    else:
        row = np.shape(detections)[0]
        for r in range(row):
            detection_result = detections[r][0]
            if detection_result == "person":
                monitor = str(1)
            else:
                monitor = str(0)

    return monitor
                    

def start_process(cap,save_img_dir,save_result_dir,width,height,network,class_names,class_colors,threshold):
    flag = True
    
    print("--------------------------------------------------------------------------------")

        
    start_time = time.time()
    
    while True:
        with open('state.json', 'r') as fr:
            state_json_file = json.load(fr)
        
        #print(state_json_file["state"])
        #print(state_json_file["state"] == "1")
        if state_json_file["state"] == "1":
        
            ret, frame = cap.read()
            dt_now = datetime.datetime.now()
            date = dt_now.strftime('%Y%m%d_%H%M%S')            
            save_result_path = str(save_result_dir + date + ".jpg")
            save_img_path = str(save_img_dir + date + ".jpg")
            cv2.imwrite(save_img_path,frame)

            if flag == True:
                image, detections = image_detection(save_img_path, network, class_names, class_colors, threshold,save_result_path,width,height)

                if len(detections) == 0:
                    monitor = str(0)

                else:
                    row = np.shape(detections)[0]
                    for r in range(row):
                        detection_result = detections[r][0]
                        if detection_result == "person":
                            monitor = str(1)
                        else:
                            monitor = str(0)

                jphack_dict = {"person": monitor}
                with open('jphack.json', 'w') as fw:
                    json.dump(jphack_dict, fw, ensure_ascii=False)

                flag = False

            elapsed_time = time.time() - start_time

            if elapsed_time >= int(5):
                flag = True
                start_time = time.time()
        
        elif state_json_file["state"] == "0":
            print("finish YOLO")
            break
            
        
            
def ready_yolo():
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = Value('i', 0)
    stop_count = Value('i', 0)
    
    weights_path = "yolov4.weights"
    cfg_path = "cfg/yolov4.cfg"
    data_path = "cfg/coco.data"
    threshold = 0.25

    network, class_names, class_colors = darknet_jphack.load_network(
        cfg_path,
        data_path,
        weights_path,
        batch_size=1
    )

    width = darknet_jphack.network_width(network)
    height = darknet_jphack.network_height(network)

    global metaMain, netMain, altNames
    altNames = None
    altNames = classname_management(altNames,data_path)
    num_classes = len(altNames)
    color_management(num_classes,class_colors,altNames)
    

    
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y%m%d_%H%M%S')
    save_img_dir = "jphack/video/" + date
    save_result_dir = "jphack/result/" + date
    os.makedirs(save_img_dir, exist_ok=True)
    os.makedirs(save_result_dir, exist_ok=True)
    save_img_dir = save_img_dir + "/"
    save_result_dir = save_result_dir + "/"

    start_process(cap,save_img_dir,save_result_dir,width,height,network,class_names,class_colors,threshold)
        

