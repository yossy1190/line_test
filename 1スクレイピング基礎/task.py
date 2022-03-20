
from selenium import webdriver
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


# def set_driver(hidden_chrome: bool=False):
#     '''
#     Chromeを自動操作するためのChromeDriverを起動してobjectを取得する
#     '''
#     USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
#     options = ChromeOptions()

#     # ヘッドレスモード（画面非表示モード）をの設定
#     if hidden_chrome:
#         options.add_argument('--headless')

#     # 起動オプションの設定
#     options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
#     options.add_argument('log-level=3') # 不要なログを非表示にする
#     options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする
#     options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする
#     options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする
#     options.add_argument('--incognito') # シークレットモードの設定を付与
    
#     # ChromeのWebDriverオブジェクトを作成する。
#     service=Service(ChromeDriverManager().install())
#     return Chrome(service=service, options=options)

def main():
    df=pd.DataFrame()
    driver_path=ChromeDriverManager().install()
    options=ChromeOptions()
    # options.add_argument("--headless")
    options.add_experimental_option('detach',True)
    driver=Chrome(driver_path,options=options)
    driver.get("https://gyoumu-kouritsuka-pro.site/")
    # options = Options()
    # options.add_experimental_option('detach', True)
    # driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(executable_path="./chromedriver.exe")

    while True:
        article_elms=driver.find_elements_by_css_selector(".entry-card-wrap.a-wrap.border-element.cf")
        for article_elm in article_elms:
            title=article_elm.find_element_by_tag_name("h2").text
            post_date=article_elm.find_element_by_css_selector(".post-date").text
            article_link=article_elm.get_attribute("href")
            print(title,post_date,article_link)

            df=df.append({
                "タイトル" : title,
                "投稿日" : post_date,
                "リンク" : article_link
            },ignore_index=True)

        try:
            driver.find_element_by_css_selector(".pagination-next-link.key-btn").click()
        except:
            print("最終ページです")
            break

    df.to_csv("記事一覧.csv",encoding="utf-8_sig")


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
