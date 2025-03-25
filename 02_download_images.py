import requests

# list.txtファイルを開く
with open("image_lists.txt", "r") as file:
    # 各行を読み込む
    for index, line in enumerate(file):
        url = line.strip()  # URLの前後の空白を削除
        try:
            # URLからコンテンツを取得
            response = requests.get(url)
            response.raise_for_status()  # HTTPエラーが発生した場合は例外を発生させる

            # 画像をjpgとして保存
            with open(f"image_{index}.jpg", "wb") as img_file:
                img_file.write(response.content)
            print(f"image_{index}.jpg を保存しました。")
        except requests.exceptions.RequestException as e:
            print(f"URL {url} の取得中にエラーが発生しました: {e}")
