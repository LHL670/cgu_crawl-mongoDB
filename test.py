import socket
import requests
from bs4 import BeautifulSoup
     

url = 'https://scholar.google.com.tw/citations?hl=zh-TW&user=' + '-R9N-K4AAAAJ'
r = requests.get(url)
soup = BeautifulSoup(r.text,features="html.parser")   
print('test')
d = soup.find('div', id='gsc_prf_i')
try:
    print(d.find('div', id='gsc_prf_in').text)
except:
    print('None')
