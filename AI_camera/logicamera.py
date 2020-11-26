import cv2
from datetime import datetime
import os


def main():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print(width,height,fps)

    jphack_dir = "jphack"
    camera_dir = "jphack/camera"   

    if not os.path.isdir(jphack_dir):
        os.makedirs(jphack_dir)
        
    if not os.path.isdir(camera_dir):
        os.makedirs(camera_dir)
        
    while True:
        ret, frame = cap.read()
        cv2.imshow("camera", frame)

        k = cv2.waitKey(1)&0xff # キー入力を待つ
        if k == ord('s'):
            # 「s」キーで画像を保存
            date = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = camera_dir + date + ".jpg"
            cv2.imwrite(path, frame) # ファイル保存

            cv2.imshow(path, frame) # キャプチャした画像を表示
        elif k == ord('q'):
            # 「q」キーが押されたら終了する
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()