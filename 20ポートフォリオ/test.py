from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def set_driver(hidden_chrome: bool=False):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    options = ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
    options.add_argument('--incognito') # シークレットモードの設定を付与
    service=Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)

def search_word():
    search_word=input("検索ワードを入力してください>>>")
    driver=set_driver()
    driver.get("https://www.lancers.jp/work/search/")
    time.sleep(2)
    driver.find_element(by=By.ID, value="Keyword").send_keys(search_word)
    driver.find_element(by=By.ID, value="Search").click()
    time.sleep(3)
    '''
    ここがうまくいきません↓
    '''
    driver.find_element(by=By.CSS_SELECTOR, value=".pager__item--next").click()
        
search_word()