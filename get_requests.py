import time
from urllib import response
from wsgiref.headers import Headers
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def urlcontent(id):
    headers={
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
              "cookie" : "NID=511=euI2V1mkdtcQ_5oHUPHxzdop5ZSxnJCPsK4S3LtFLhyHumHL2zUS0-Lf_Dx91Oz2H-h513-b3YphJ_vXYqVJ0QpCegfVo1OAgku47ZQht472C8ZUytRt1P_3S1EmwT7JLfBlVGms8Y_eEOh5SPeiaZtOiGVjFW6POvU1FEgo1dk"
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

            response = session.get(url, headers=headers, allow_redirects=True)
            
            break
        except Exception as e:
            print("request error.sleep 10 second and restart" + str(e))
            time.sleep(10)
            continue

    if response.status_code == requests.codes.ok:
        
        return response.url    
