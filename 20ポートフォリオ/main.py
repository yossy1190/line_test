from encodings import utf_8_sig
from operator import index
import os
from xml.sax.handler import property_xml_string
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import pandas as pd
import numpy as np


# Selenium4対応済

def set_driver(hidden_chrome: bool=False):
    '''
    Chromeを自動操作するためのChromeDriverを起動してobjectを取得する
    '''
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if hidden_chrome:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
    options.add_argument('log-level=3') # 不要なログを非表示にする
    options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする
    options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする
    options.add_argument('--incognito') # シークレットモードの設定を付与
    
    # ChromeのWebDriverオブジェクトを作成する。
    service=Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)

LOG_FILE_PATH="logs/log_{datetime}.log"
EXP_CSV_PATH="results/exp_list_{search_keyword}_{datetime}.csv"
log_file_path=LOG_FILE_PATH.format(datetime=datetime.datetime.now)
# .strftime('%Y-%m-%d-%H-%M-%S')

def makedir_for_filepath(filepath:str):
    os.makedirs(os.path.dirname(filepath),exist_ok=True)
# makedirsを使うことでフォルダを新規作成。os.path.dirname(XXX)でXXXという名前のフォルダを新規作成

def log(txt):
    now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr='[%s: %s] %s' % ('log',now , txt)
    makedir_for_filepath(log_file_path)
    with open(log_file_path,"a",encoding="utf-8_sig") as f:
        f.write(logStr+"\n")
    print(logStr)

def main():
    # Webサイトを開く
    driver.get("https://www.lancers.jp/work/search/")
    # search のあとに、system や webなどをくっつけること遷移可能
    
    time.sleep(3)
    # https://www.lancers.jp/work/search?open=1&show_description=0&work_rank%5B%5D=0&work_rank%5B%5D=1&work_rank%5B%5D=2&work_rank%5B%5D=3
    # https://www.lancers.jp/work/search?open=1&work_rank%5B%5D=3&work_rank%5B%5D=2&work_rank%5B%5D=1&work_rank%5B%5D=0&budget_from=&budget_to=&search=%E6%A4%9C%E7%B4%A2&keyword=%E3%83%A9%E3%82%A4%E3%82%BF%E3%83%BC&not=
    '''
    ポップアップを閉じる
    ※余計なポップアップが操作の邪魔になる場合がある
      モーダルのようなポップアップ画面は、通常のclick操作では処理できない場合があるため
      excute_scriptで直接Javascriptを実行することで対処する
    '''
    try:
        driver.execute_script('document.querySelector(".Commonstyled__PreviewCloseButton-sc-1uivlpa-3.jOVdaf").click()')
        time.sleep(5)
    except:
        print("ポップアップなし")
    # ポップアップを閉じる
    '''
    find_elementでHTML要素(WebElement)を取得する
    byで、要素を特定する属性を指定するBy.CLASS_NAMEの他、By.NAME、By.ID、By.CSS_SELECTORなどがある
    特定した要素に対して、send_keysで入力、clickでクリック、textでデータ取得が可能
    '''
    # 検索窓に入力
    driver.find_element(by=By.CLASS_NAME, value="c-basic-search__keyword").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element(by=By.CLASS_NAME, value="c-basic-search__submit.c-icon-button.c-icon-button--blue").click()


    '''
    find_elements(※複数形)を使用すると複数のデータがListで取得できる
    一覧から同一条件で複数のデータを取得する場合は、こちらを使用する
    '''
    
    # 空のリスト作成
    job_items=[]

    # 1ページ分繰り返し
    # print(len(name_elms))
    '''
    name_elmsには１ページ分の情報が格納されているのでforでループさせて１つづつ取り出して、Dataframeに格納する
    '''
    
    while True:
        title_elms= driver.find_elements(by=By.CLASS_NAME, value="c-media__title-inner")
        payment_elms=driver.find_elements(by=By.CLASS_NAME,value="c-media__job-price")
        # proposes=driver.find_elements(by=By.CLASS_NAME,value="c-media__job-propose")
        # jobs=driver.find_elements(by=By.CLASS_NAME,value="c-media__title")
        # jobs_links=jobs[0].__getattribute__("href")
        #  = driver.find_elements_by_css_selector(".cassetteRecruit__copy.boxAdjust")
    
        for title_elm,payment_elm in zip(title_elms,payment_elms):
            
            # propose=propose.find_elements(by=By.CLASS_NAME,value="c-media__job-number")
            print(title_elm.text,payment_elm.text)
            # DataFrameに対して辞書形式でデータを追加する
            job_items.append(
                {"案件名": title_elm.text, 
                "報酬額": payment_elm.text,
                # "案件リンク":propose.text
                }, 
                )
        
        try:
            driver.find_element_by_css_selector(".pager__item__anchor").click()
        
        except:
            print("最終ページです。")
            break
    df=pd.DataFrame.from_dict(job_items,dtype=object)
    df.index=df.index+1
    df.to_csv("案件情報一覧.csv",encoding="utf_8_sig")
    
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()