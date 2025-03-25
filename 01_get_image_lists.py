import os
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)

    try:
        login_to_site(browser)
        navigate_to_album(browser)
        output_links = collect_image_links(browser)
        save_links_to_file(output_links)
    finally:
        input("続行するにはEnterキーを押してください...")

def login_to_site(browser):
    """サイトにログインする"""
    browser.get(url_login)
    browser.find_element(By.NAME, "data[mail]").send_keys(ID)
    browser.find_element(By.NAME, "data[password]").send_keys(PASS)
    browser.find_element(By.NAME, "mode_login").click()

def navigate_to_album(browser):
    """アルバムページに移動する"""
    browser.get(url_room)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "categoryBtn"))
    ).click()
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, text_album))
    ).click()

def collect_image_links(browser):
    """画像リンクを収集する"""
    output_links = []
    for _ in range(99):
        output_links += get_url(browser)
        if not go_to_next_page(browser):
            break
    return output_links

def go_to_next_page(browser):
    """次のページに移動する"""
    try:
        next_link = browser.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
        browser.get(next_link.get_attribute("href"))
        return True
    except NoSuchElementException:
        print("次のページはありません")
        return False

def get_url(browser):
    """現在のページから画像リンクを取得する"""
    photo_list_inner = browser.find_element(By.ID, "photoListInner")
    photo_boxes = photo_list_inner.find_elements(By.CSS_SELECTOR, "div.photoBox")

    image_links = []
    for photo_box in photo_boxes:
        try:
            first_div = photo_box.find_element(By.CSS_SELECTOR, "div.inner > div")
            first_div.click()
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#imageWrap > img"))
            )
            image_src = browser.find_element(By.CSS_SELECTOR, "#imageWrap > img").get_attribute("src")
            image_links.append(image_src + "\n")
            close_image_modal(browser)
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    return image_links

def close_image_modal(browser):
    """画像モーダルを閉じる"""
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#modalHeader > span.close"))
    ).click()
    WebDriverWait(browser, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "#modalHeader > span.close"))
    )

def save_links_to_file(links):
    """リンクをファイルに保存する"""
    with open("./image_lists.txt", "w") as file:
        file.writelines(links)

if __name__ == "__main__":
    main()