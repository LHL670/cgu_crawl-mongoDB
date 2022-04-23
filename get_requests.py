from time import time
import requests
from bs4 import BeautifulSoup


def urlcontent(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36','Connention':'close'
    }
    while 1:    
        try:
            r = requests.get(url, headers=headers, proxies={
                            "https": "http://0.0.0.0:8888"}).text
            break
        except:
            print("request error.sleep 1 min and restart")
            time.sleep(60)
            continue
    
    soup = BeautifulSoup(r, "html.parser")
    return soup

