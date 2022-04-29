
import requests
import time
import json
def getcurrentIP():
    url = 'http://httpbin.org/ip'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    ip = requests.get(url, headers=headers, proxies={
                            "http": "http://0.0.0.0:8888"}).text
    
    ip = json.loads(ip)
    # print(type(ip))

    return ip['origin']
        
#  {
#   "origin": "5.2.69.50"
# }
           

def detectIPchange():
    originIP = getcurrentIP()
    newIP = originIP
    while 1:
        time.sleep(1)
        newIP = getcurrentIP()
        if originIP == newIP:
            break
        else:
            originIP = newIP

    return 

# if __name__ == '__main__':
#     print('start')
#     detectIPchange()
#     print('done')