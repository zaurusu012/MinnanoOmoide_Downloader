# Image Link Collector and Downloader

このプロジェクトは、指定されたウェブサイトにログインし、特定のアルバムページから画像リンクを収集し、その画像をダウンロードするためのスクリプトを提供します。

## 必要条件

- Python 3.x
- Selenium
- ChromeDriver
- requests
- 環境変数 `LOGIN_ID` と `LOGIN_PASS` にログイン情報を設定
- `url_room`を展示室のurlに書き換える
- `text_album`をアルバム名に書き換える

## インストール

1. 必要なPythonパッケージをインストールします。

   ```bash
   pip install selenium requests
   ```

2. [ChromeDriver](https://sites.google.com/chromium.org/driver/) をダウンロードし、システムのPATHに追加します。

## 環境変数の設定

スクリプトを実行する前に、以下の環境変数を設定してください。

- `LOGIN_ID`: ログインに使用するメールアドレス
- `LOGIN_PASS`: ログインに使用するパスワード

例（Linux/Mac）:

```bash
export LOGIN_ID="your_email@example.com"
export LOGIN_PASS="your_password"
```

例（Windows）:

```cmd
set LOGIN_ID=your_email@example.com
set LOGIN_PASS=your_password
```

## 使用方法

1. 画像リンクを収集するために、`01_get_image_lists.py` を実行します。

   ```bash
   python 01_get_image_lists.py
   ```

   - スクリプトが完了すると、`image_lists.txt` ファイルに画像リンクが保存されます。

2. 収集したリンクから画像をダウンロードするために、`02_download_images.py` を実行します。

   ```bash
   python 02_download_images.py
   ```

   - 各画像は `image_0.jpg`, `image_1.jpg`, ... のように保存されます。

## 注意事項

- スクリプトは、指定されたアルバムページから最大99ページ分の画像リンクを収集します。
- ウェブサイトの構造が変更された場合、スクリプトが正常に動作しない可能性があります。その場合は、セレクタやURLを更新してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。