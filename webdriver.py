from selenium import webdriver  # 從library中引入webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


def test(id):
    url = 'https://scholar.google.com.tw/citations?hl=zh-TW&user=' + id + '&pagesize=100'
    chrome_options = Options()
    driver = webdriver.Chrome()
    driver.maximize_window()
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
                    soup = BeautifulSoup(driver.page_source)
                    driver.quit()
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
