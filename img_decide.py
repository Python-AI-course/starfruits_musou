import sys
import os
import cv2
import keras
import numpy as np
import matplotlib.pyplot as plt
import settings

def detect_face(model, cascade_filepath, image):
    # 画像をBGR形式からRGB形式へ変換
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # plt.imshow(image)
    # plt.show()
    # print(image.shape)
    # グレースケール画像へ変換
    image_gs = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # 顔認識の実行
    cascade = cv2.CascadeClassifier(cascade_filepath)
    face_list = cascade.detectMultiScale(image_gs, scaleFactor=1.1,
                                         minNeighbors=2, minSize=(64, 64))

    # 顔が１つ以上検出できた場合
    if len(face_list) > 0:
        print(f"認識した顔の数:{len(face_list)}")
        for (xpos, ypos, width, height) in face_list:
            # 認識した顔の切り抜き
            face_image = image[ypos:ypos+height, xpos:xpos+width]
            print(f"認識した顔のサイズ:{face_image.shape}")
            if face_image.shape[0] < 64 or face_image.shape[1] < 64:
                print("認識した顔のサイズが小さすぎます。")
                continue
            # 認識した顔のサイズ縮小
            face_image = cv2.resize(face_image, (64, 64))
            # plt.imshow(face_image)
            # plt.show()
            # print(face_image.shape)
            # 認識した顔のまわりを赤枠で囲む
            cv2.rectangle(image, (xpos, ypos), (xpos+width, ypos+height),
                          (255, 0, 0), thickness=2)
            # 認識した顔を1枚の画像を含む配列に変換
            face_image = np.expand_dims(face_image, axis=0)
            # 認識した顔から名前を特定
            name = detect_who(model, face_image)
            # 認識した顔に名前を描画
            cv2.putText(image, name, (xpos, ypos+height+20),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
    # 顔が検出されなかった時
    else:
        print(f"顔を認識できません。")
    return image

def detect_who(model, face_image):
    # 予測
    name = ""
    result = model.predict(face_image)
    print(f"スギちゃん　 の可能性:{result[0][0]*100:.3f}%")
    print(f"オードリー春日　の可能性:{result[0][1]*100:.3f}%")
    name_number_label = np.argmax(result)
    if name_number_label == 0:
        name = "sugityan"
    elif name_number_label == 1:
        name = "kasuga"
    return name

RETURN_SUCCESS = 0
RETURN_FAILURE = -1
# Inpou Model Directory
INPUT_MODEL_PATH = "./model/model.h5"

def main():
    print("===================================================================")
    print("顔認識 Keras 利用版")
    print("学習モデルと指定した画像ファイルをもとに本田翼か佐倉綾音かを分類します。")
    print("===================================================================")

    # 引数のチェック
    argvs = sys.argv
    if len(argvs) != 2 or not os.path.exists(argvs[1]):
        print("画像ファイルを指定して下さい。")
        return RETURN_FAILURE
    image_file_path = argvs[1]

    # 画像ファイルの読み込み
    image = cv2.imread(image_file_path)
    if image is None:
        print(f"画像ファイルを読み込めません。{image_file_path}")
        return RETURN_FAILURE

    # モデルファイルの読み込み
    if not os.path.exists(INPUT_MODEL_PATH):
        print("モデルファイルが存在しません。")
        return RETURN_FAILURE
    model = keras.models.load_model(INPUT_MODEL_PATH)

    # 顔認識
    cascade_filepath = settings.CASCADE_FILE_PATH
    result_image = detect_face(model, cascade_filepath, image)
    plt.imshow(result_image)
    plt.show()

    return RETURN_SUCCESS

if __name__ == "__main__":
    main()