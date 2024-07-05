import cv2
import time
from ultralytics import YOLO
from calling_api import ask_gpt

import numpy as np

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

def calculate_compatibility(results, image):
    
    # 検出された顔が2つであることを確認
    if len(results[0].boxes) != 2:
        print("検出された顔が2つではありません。")
        return np.random.randint(0, 100)

    faces = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        face = image[y1:y2, x1:x2]
        faces.append(face)

    # 顔画像のサイズを統一
    face1 = cv2.resize(faces[0], (100, 100))
    face2 = cv2.resize(faces[1], (100, 100))

    # グレースケールに変換
    gray1 = cv2.cvtColor(face1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(face2, cv2.COLOR_BGR2GRAY)

    # ヒストグラムの計算
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])

    # ヒストグラムの比較
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    # 相性スコアの計算（類似度を0-100のスケールに変換）
    compatibility_score = int(similarity * 100)

    return compatibility_score

def data_processing(image, results, conf_threshold=0.7):
    person_count = 0
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            
            if cls == 0 and conf >= conf_threshold:  # 人クラス（YOLOv8の場合、人は通常クラス0）
                person_count += 1
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f'Person: {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # 検出した人数を画像に表示
    cv2.putText(image, f'Detected: {person_count}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return image, person_count

def main():
    # YOLOv8モデルの読み込み
    model = YOLO('yolov10n.pt')
    
    # カメラの初期化
    cap = cv2.VideoCapture(0)
    
    # 認識を止めるまでの関数
    count = 0
    
    # 相性
    value = 0
    
    while True:
        # カメラからフレームを読み込む
        ret, frame = cap.read()
        if not ret:
            break
        
        # 顔の検出とトラッキング
        results = model.track(frame, persist=True)
        
        # フレームを処理
        processed_frame, person_count = data_processing(frame, results, conf_threshold=0.8)
        
        # 処理結果を表示
        cv2.imshow('Face Detection', processed_frame)
        cv2.moveWindow('Face Detection', 400, 150)
        
        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif person_count == 2:
            count += 1
            if count > 20:
                print("2人検出しました")  # 2人検出時の処理
                value = calculate_compatibility(results, frame)
                cv2.destroyAllWindows()
                time.sleep(0.1)
                break
        else:
            count = 0
    # リソースの解放
    cap.release()

    print(value)
    result = ask_gpt("ある二人の相性を測ってみたところ，その数値は0~100のうち" + str(value) + "でした。どうすれば改善できますか？二人の関係はわからなくていいので，プライベートを勝手に想像し，とにかく辛辣なことを話してください．")
    print(result)
    
    return [value, result]

 
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# グローバル変数として value_list を定義
value_list = None

@app.get("/")
async def get_compatibility():
    global value_list
    if value_list is None:
        value_list = main()
    return {"compatibility": value_list[0], "message": value_list[1]}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3001, reload=True)