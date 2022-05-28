import time
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def urlcontent(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36', 'Connention': 'close'
    }
    proxies={"https": "http://0.0.0.0:8888"}
    url = 'https://scholar.google.com.tw/citations?hl=zh-TW&user=' + id
    while 1:
        try:
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            session.proxies.update(proxies)

            res = session.get(url, headers=headers)
            res = res.text
            break
        except Exception as e:
            print("request error.sleep 10 second and restart" + str(e))
            time.sleep(10)
            continue

    soup = BeautifulSoup(res, "html.parser")
    return soup
