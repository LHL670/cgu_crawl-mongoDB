
import getTime
import queue
import manageMongodb


def get_IDqueue(label):
    print('GET label : '+str(label))
    # 建立佇列
    IDQueue = queue.Queue()

    # 將資料放入佇列

    IDtemp = manageMongodb.get_labeldomainuserIDlist(label)
    print("check userID expires start")
    for i in IDtemp:

        expire_time = manageMongodb.get_userupdatetime(i)
        if(getTime.check_expires(expire_time, 30)):
            IDQueue.put(i)
    print("check userID expires end")
    # number = number - 1
    # ID_count = ID_count + 1
    # # 取五個過期或為爬過的ID
    # number = 100
    # ID_count = 0
    # while (number != 0):
    #     expire_time = manageFirebase.get_userupdatetime(
    #         IDtemp['userID'][ID_count])
    #     if(getTime.check_expires(expire_time, 30)):
    #         print(IDtemp['userID'][ID_count])
    #         IDQueue.put(IDtemp['userID'][ID_count])
    #         number = number - 1
    #     ID_count = ID_count + 1

    return IDQueue
