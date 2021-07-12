#必要なモジュールをインポート
import os
import sys 
from flask import (
     Flask, 
     request, 
     redirect, 
     url_for, 
     make_response, 
     jsonify, 
     render_template, 
     send_from_directory)


# 画像のアップロード先のディレクトリ
UPLOAD_FOLDER_ENTER = './image_enter' #もでるの作成用
UPLOAD_FOLDER_USER_FACE = './image_user' #ユーザーが利用する写真用
FROM_PATH_TO_VECTOR = {} #画像パスとベクトルを紐つけるための空の辞書

#FlaskでAPIを書くときのおまじない
app = Flask(__name__,static_folder='image')

#アプリのホーム画面のhtmlを返すURL
@app.route('/')
def top():
    return render_template(
        'top.html',
          )

@app.route('/result')
def result():
    return render_template(
        'result.html',
        enter_images=os.listdir(UPLOAD_FOLDER_ENTER)[::-1], #[::-1]はリストの要素をが逆順で並び替え
        user_images=os.listdir(UPLOAD_FOLDER_USER_FACE)[::-1]
    )
@app.route('/upload', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'upload_files' not in request.files:
            print("ファイルなし")
            return redirect(request.url)

        if request.files.getlist('upload_files')[0].filename:
            #画像オブジェクトを受け取る。
            uploads_files = request.files.getlist('upload_files')
            for uploads_file in uploads_files:
                #それぞれの画像に対してimage_enterまでのパスを定義作成してsaveメソッドを用いて保存する。
                img_path = os.path.join(UPLOAD_FOLDER_USER_FACE, uploads_file.filename)
                uploads_file.save(img_path)
        return redirect('/result')
#ディレクトリに保存されている画像をブラウザに送る処理
@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory(UPLOAD_FOLDER_USER_FACE, path)


#スクリプトからAPIを叩けるようにします。
if __name__ == "__main__":
    app.run(debug=True)
