import os
import sys
from urllib.parse import quote
import requests
import settings

# 指定したキーワードで検索した画像のURLを取得
def get_image_urls(keyword, total_num):
    image_urls = []
    i = 0
    while i < total_num:
        # クエリの組み立て
        query = CUSTOM_SEARCH_URL + "?key=" + settings.API_KEY + \
                "&cx=" + settings.CUSTOM_SEARCH_ENGINE + "&num=" + \
                str(10 if(total_num-i) > 10 else (total_num-i)) + "&start=" + \
                str(i+1) + "&q=" + quote(keyword) + "&searchType=image"
        print(query)
        # GETリクエスト
        response = requests.get(query)
        # JSONデータ取得
        json = response.json()
        # 10件ずつのURLを格納
        for j in range(len(json["items"])):
            image_urls.append(json["items"][j]["link"])
        i = i + 10
    return image_urls

# 画像のURLをもとに画像をダウンロードして保存
def get_image_files(dir_path, keyword_count, image_urls):
    # 画像urlループ
    for (idx, image_url) in enumerate(image_urls):
        try:
            # 画像をダウンロード
            print(image_url)
            image = download_image(image_url)
            # ファイル名を作成
            filename_extension_pair = os.path.splitext(image_url)
            extension = filename_extension_pair[1]
            extension = extension if len(extension) <= 4 else extension[0:4]
            filename = os.path.join(dir_path, f"{keyword_count:02}_{idx+1:03}{extension}")
            print(filename)
            # 画像をファイルとして保存
            save_image(filename, image)
        except RuntimeError as ex:
            print(f"type:{type(ex)}")
            print(f"args:{ex.args}")
            print(f"{ex}")
            continue
        except BaseException as ex:
            print(f"type:{type(ex)}")
            print(f"args:{ex.args}")
            print(f"{ex}")
            continue

# 画像をダウンロード
def download_image(url):
    response = requests.get(url, timeout=100)
    if response.status_code != 200:
        raise RuntimeError("画像が取得できません")
    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        raise RuntimeError("画像ではありません")
    return response.content

# 画像をファイルとして保存
def save_image(filename, image):
    with open(filename, "wb") as file:
        file.write(image)

# ディレクトリまたはディレクトリ内のファイル削除
def delete_dir(dir_path, is_delete_top_dir=True):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    if is_delete_top_dir:
        os.rmdir(dir_path)

RETURN_SUCCESS = 0
RETURN_FAILURE = -1
# Custom Search Url
CUSTOM_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"
# Download Directory Path
ORIGIN_IMAGE_DIR = "./origin_image"

def main():
    print("===================================================================")
    print("イメージダウンローダー Google Customr Search API 版")
    print("指定したキーワードで検索した画像ファイルをダウンロードします。")
    print("===================================================================")

    # 引数のチェック
    argvs = sys.argv
    if len(argvs) != 2 or not argvs[1]:
        print("キーワードを指定してください。（カンマ区切り可能）")
        return RETURN_FAILURE

    # キーワードの取得
    keywords = [x.strip() for x in argvs[1].split(',')]

    # ディレクトリの作成
    if not os.path.isdir(ORIGIN_IMAGE_DIR):
        os.mkdir(ORIGIN_IMAGE_DIR)
    delete_dir(ORIGIN_IMAGE_DIR, False)

    # キーワードごとに画像ファイル取得
    keyword_count = 1
    for keyword in keywords:
        # キーワード表示
        print(f"キーワード「{keyword}」で検索した画像ファイルをダウンロードします。")
        # 画像URL取得
        image_urls = get_image_urls(keyword, 100)
        # 画像ファイルのダウンロード
        get_image_files(ORIGIN_IMAGE_DIR, keyword_count, image_urls)
        # カウントアップ
        keyword_count = keyword_count + 1

    return RETURN_SUCCESS

if __name__ == "__main__":
    main()