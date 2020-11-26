import argparse
import os
import glob
import random
import darknet
import time
import cv2
import numpy as np
import darknet_jphack
from datetime import datetime

#YOLOの物体検出に必要なファイルや条件指定
def parser():
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--input", type=str, default="",
                        help="image source. It can be a single image, a"
                        "txt with paths to them, or a folder. Image valid"
                        " formats are jpg, jpeg or png."
                        "If no input is given, ")
    parser.add_argument("--batch_size", default=1, type=int,
                        help="number of images to be processed at the same time")
    parser.add_argument("--weights", default=weights_path,
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true',
                        help="display bbox coordinates of detected objects")
    parser.add_argument("--save_labels", action='store_true',
                        help="save detections bbox for each image in yolo format")
    parser.add_argument("--config_file", default=cfg_path,
                        help="path to config file")
    parser.add_argument("--data_file", default=data_path,
                        help="path to data file")
    parser.add_argument("--thresh", type=float, default=threshold,
                        help="remove detections with lower confidence")
    return parser.parse_args()

#デバッグ
def check_arguments_errors(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config_file):
        raise(ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))
    if not os.path.exists(args.weights):
        raise(ValueError("Invalid weight path {}".format(os.path.abspath(args.weights))))
    if not os.path.exists(args.data_file):
        raise(ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))
    if args.input and not os.path.exists(args.input):
        raise(ValueError("Invalid image path {}".format(os.path.abspath(args.input))))

#YOLOによる物体検出
def image_detection(image_path, network, class_names, class_colors, thresh,save_result_path):
    #画像読み込み
    image = cv2.imread(image_path)
    #物体検出のための画像の前処理
    darknet_image = darknet_jphack.make_image(width, height, 3)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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

#任意のタイミングで物体検出をしてその結果を保存する
def main():
    
    while True:
        ret, frame = cap.read()
        cv2.imshow("camera", frame)
        
        k = cv2.waitKey(1)&0xff # キー入力を待つ
        
        # 「s」キーで画像を保存＆物体検出
        if k == ord('s'):
            #画像のパス生成
            date = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = img_dir + date + ".jpg"
            save_result_path = str(img_dir + date + "_result.jpg")
            #画像保存
            cv2.imwrite(path, frame)
            #YOLOによる物体検出
            image, detections = image_detection(path, network, class_names, class_colors, args.thresh,save_result_path)
            
        # 「q」キーが押されたら終了する    
        elif k == ord('q'):
            break


if __name__ == "__main__":
    #カメラ起動
    cap = cv2.VideoCapture(0)
    
    #YOLOの物体検出に必要なファイルのパス
    weights_path = "yolov4-tiny.weights"
    cfg_path = "cfg/yolov4-tiny.cfg"
    data_path = "cfg/coco.data"
    threshold = 0.25  
    
    #画像を保存するディレクトリ
    jphack_dir = "jphack"
    img_dir = "jphack/img_test"
    #ディレクトリがない場合にディレクトリ作成
    if not os.path.isdir(img_dir):
        os.makedirs(img_dir)
    if not os.path.isdir(img_dir):
        os.makedirs(img_dir)
        
    #デバッグ
    args = parser()
    check_arguments_errors(args)
    #枠の色をランダムで決定
    random.seed(3)
    
    #CNNやデータのロード
    network, class_names, class_colors = darknet_jphack.load_network(
        args.config_file,
        args.data_file,
        args.weights,
        batch_size=args.batch_size
    )
    #検出結果の画像サイズ
    width = darknet_jphack.network_width(network)
    height = darknet_jphack.network_height(network)
    
    #任意のタイミングで物体検出をしてその結果を保存する
    main()
