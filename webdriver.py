from selenium import webdriver  # 從library中引入webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
# from selenium.webdriver.common.proxy import Proxy, ProxyType


def Firefoxwebdriver(id):
    url = 'https://scholar.google.com.tw/citations?hl=zh-TW&user=' + id + '&pagesize=100'
    # chrome_options = Options()
    options = Options()
    options.add_argument('--headless')
    # myProxy = '0.0.0.0:9050'
    # ip, port = myProxy.split(":")
    # driver = webdriver.FirefoxProfile()
    # driver.set_preference('network.proxy.type', 1)
    # driver.set_preference('network.proxy.socks', ip)
    # driver.set_preference('network.proxy.socks_port', int(port))
    # driver = webdriver.Firefox(driver,options=options)
    myProxy = '0.0.0.0:8888'
    ip, port = myProxy.split(":")
    driver = webdriver.FirefoxProfile()
    driver.set_preference('network.proxy.type', 1)
    driver.set_preference('network.proxy.http', ip)
    driver.set_preference('network.proxy.http_port', int(port))
    driver.set_preference("network.proxy.share_proxy_settings", True)
    driver.set_preference("network.http.use-cache", False)
    driver.update_preferences()
    
    driver = webdriver.Firefox(firefox_profile=driver,options=options)
    # driver = webdriver.Firefox()
    # driver.maximize_window()
    driver.implicitly_wait(8)  # set waiting time

    driver.get(url)
    while True:
        try:
            tempcount = 0
            # the button which shows more detail
            element = driver.find_element(By.XPATH, '//*[@id="gsc_bpf_more"]')

            while element.get_property('disabled'):
                tempcount = tempcount + 1
                time.sleep(0.05)

                # the end of the page
                if tempcount > 50:
                    soup = BeautifulSoup(driver.page_source,"html.parser")
                    driver.quit()
                    time.sleep(0.1)
                    return soup
            try:
                element.click()
            except:
                continue
        except:
            driver.quit()
            break
    soup = BeautifulSoup(driver.page_source)
    return soup
# def get_articles(soup):
#     Articles = []
#     paperblock = soup.find('tbody', id='gsc_a_b').find_all(
#         'tr', class_='gsc_a_tr')

#     # for papers in range(len(paperblock)):
#     return len(paperblock)    
# print(get_articles(Firefoxwebdriver('UF2gBtMAAAAJ')))