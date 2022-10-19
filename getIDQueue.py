import time
from typing import Collection
import getTime
import queue
import manageMongodb


def get_IDqueue_forprofile(label):
    print('GET label : '+str(label))
    # 建立佇列
    IDQueue = queue.Queue()

    # 將資料放入佇列

    IDtemp = manageMongodb.get_labeldomainuserIDlist(label)
    print("check userID expires start")
    collection = 'cguscholar'
    for i in IDtemp:

        expire_time = manageMongodb.get_userupdatetime(i,collection)
        if(getTime.check_expires(expire_time, 7)):
            IDQueue.put(i)
    print("check userID expires end")
    return IDQueue

def get_IDqueue_forarticles():
    # 建立佇列
    IDQueue = queue.Queue()

    # 將資料放入佇列

    IDtemp = manageMongodb.get_userIDforarticlesupdate()
    print("check user articles expires start")
    collection = 'articles'
    for i in IDtemp:

        expire_time = manageMongodb.get_userupdatetime(i,collection)
        if(getTime.check_expires(expire_time, 2)):
            IDQueue.put(i)
        time.sleep(0.01)
    print("check user articles expires end")
    return IDQueue