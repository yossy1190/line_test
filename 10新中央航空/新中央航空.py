import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def main():
    driver_path = ChromeDriverManager().install()
    chromeServices = Service(executable_path=driver_path) # os.getcwd()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(driver_path,service=chromeServices, options=options)
    driver.get('https://www.central-air.co.jp/reservation/ibe/ibe/booking')
    sleep(1)
    
    '''
    日付選択までの画面
    
    '''    
    ##
    from_xpath = "//select[@id='aiRESOrigin']"
    from_element = driver.find_element(By.XPATH, from_xpath)
    select_from = Select(from_element)
    select_from.select_by_value('CHU')
    
    ##
    to_xpath = "//select[@id='aiRESDestination']"
    to_element = driver.find_element(By.XPATH, to_xpath)
    select_from = Select(to_element)
    select_from.select_by_value('OIM')
    
    search_date = "2022/03/25"

    date_xpath = "//input[@id='travelDate#trvDate_1']"
    date_element = driver.find_element(By.XPATH, date_xpath)
    date_element.click()
    date_element.clear()
    date_element.send_keys(search_date)
  
    send_xpath = "//input[@id='proceed']"
    send_element = driver.find_element(By.XPATH, send_xpath)
    send_element.click()
    sleep(3)

    '''
    日付選択後の画面
    
    '''    
    
    
    flight_non=driver.find_element_by_id("0_29-Mar-2022_0_0")
    searchradios=flight_non.find_elements_by_css_selector(".searchfareradio")
    # searchfaradiosからimg srcを取り出す。searchfareradiosは、複数あるので、注意
    img src="/reservation/ja/images/cg.png"
    
    
    
    # flight_table_xpath = "//table[@id='flightrows']"
    # flithg_table = driver.find_element(By.XPATH, flight_table_xpath)
    # for tr in data_trs:
    #     try:
    #         flight_no = tr.find_element(By.CLASS_NAME, 'searchfltno').text
    #     except:
    #         flight_no = "-"
    #     try:
    #         flight_boardpt = tr.find_element(By.CLASS_NAME, 'searchboardpt').text
    #     except:
    #         flight_boardpt = "-"
    #     try:
    #         flight_arrTime = tr.find_element(By.CLASS_NAME, 'searcharrTime.wth_15').text
    #     except:
    #         flight_arrTime = "-"
            
    #     if flight_no != '-':
    #         print(f"[{search_date}] flight No:{flight_no}, {flight_boardpt} - {flight_arrTime}")

if __name__ =="__main__":
    main()
    