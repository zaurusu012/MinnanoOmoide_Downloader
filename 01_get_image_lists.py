import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# ログイン情報
ID = os.getenv("LOGIN_ID")
PASS = os.getenv("LOGIN_PASS")

url_login = "https://ps.happysmile-inc.jp/sys/UserLogin"
url_room = "https://ps.happysmile-inc.jp/sys/UserRoom/index/271336"
text_album = "ぱんだ(157)"


def main():
    # ブラウザのドライバーを得る
    browser = webdriver.Chrome()  # ChromeDriverを使用
    browser.implicitly_wait(10)

    try:
        # ログインページ
        browser.get(url_login)
        id_input = browser.find_element(By.NAME, "data[mail]")
        pass_input = browser.find_element(By.NAME, "data[password]")
        login_button = browser.find_element(By.NAME, "mode_login")

        id_input.clear()
        pass_input.clear()
        id_input.send_keys(ID)
        pass_input.send_keys(PASS)
        login_button.click()

        # 展示室
        browser.get(url_room)
        id_btn = "categoryBtn"
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, id_btn))
        )
        category_button = browser.find_element(By.ID, id_btn)
        category_button.click()

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, text_album))
        )
        album_link = browser.find_element(By.LINK_TEXT, text_album)
        album_link.click()

        # 画像リンクを保存するリスト
        output_links = []

        # break文を使った例
        for _ in range(99):  # 99ループを設定
            output_links += get_url(browser)
            try:
                next_link = browser.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
                href_value = next_link.get_attribute("href")  # href属性の値を取得
                browser.get(href_value)
                # WebDriverWait(browser, 10).until(
                #    EC.presence_of_element_located((By.LINK_TEXT, href_value))
                # )

            except NoSuchElementException:
                try:
                    # <span class="next disabled">要素を探す
                    disabled_next = browser.find_element(
                        By.CSS_SELECTOR, "span.next.disabled"
                    )
                    print("次のページはありません: ", disabled_next.text)
                    break
                except NoSuchElementException:
                    print(
                        'rel="next"要素も<span class="next disabled">要素も見つかりませんでした。'
                    )
                    break

        # リストの内容をファイルに書き込む
        with open("./image_lists.txt", "w") as file:
            file.writelines(output_links)
    finally:
        input("続行するにはEnterキーを押してください...")


def get_url(browser):
    # アルバムページ
    photo_list_inner = browser.find_element(By.ID, "photoListInner")
    photo_boxes = photo_list_inner.find_elements(By.CSS_SELECTOR, "div.photoBox")
    # print(len(photo_boxes))

    image_links = []
    for photo_box in photo_boxes:
        try:
            # 画像を開く
            first_div = photo_box.find_element(By.CSS_SELECTOR, "div.inner > div")
            first_div.click()
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#imageWrap > img"))
            )
            image_element = browser.find_element(By.CSS_SELECTOR, "#imageWrap > img")
            image_src = image_element.get_attribute("src")

            # 画像のリンクをリストに追加
            image_links.append(image_src + "\n")

            # 画像を閉じる
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#modalHeader > span.close")
                )
            )
            close_button = browser.find_element(
                By.CSS_SELECTOR, "#modalHeader > span.close"
            )
            close_button.click()
            WebDriverWait(browser, 10).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "#modalHeader > span.close")
                )
            )

            # print(f"Clicked on div with ID: {first_div.get_attribute('id')}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    return image_links


if __name__ == "__main__":
    main()
