import cv2
from datetime import datetime
import os

#カメラ動作確認
def main():
    #カメラ起動
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    #カメラのプロパティの表示
    print(width,height,fps)

    #画像を保存するディレクトリ
    jphack_dir = "jphack"
    camera_dir = "jphack/camera"   
    #ディレクトリがない場合にディレクトリ作成
    if not os.path.isdir(jphack_dir):
        os.makedirs(jphack_dir)       
    if not os.path.isdir(camera_dir):
        os.makedirs(camera_dir)
        
    #カメラからの映像を取得
    while True:
        #カメラからの映像を取得
        ret, frame = cap.read()
        #カメラからの映像を画面に表示
        cv2.imshow("camera", frame)

        k = cv2.waitKey(1)&0xff
        
        # 「s」キーで画像を保存
        if k == ord('s'):
            #画像のパス生成
            date = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = camera_dir + date + ".jpg"
            # 画像保存
            cv2.imwrite(path, frame) 
            # 画像を表示
            cv2.imshow(path, frame) 
            
        # 「q」キーが押されたら終了する
        elif k == ord('q'):          
            break
            
    #カメラ停止
    cap.release()
    #表示していた画面を終了
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #カメラ動作確認
    main()