from itertools import count

import pymongo
from pymongo import MongoClient
import jsonTransfer
cluster = MongoClient(
    "mongodb+srv://CGUScholar:cguscholarpwd@cluster0.bpq9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["CGUScholar"]

collection = db["test"]

# 更新userprofile


def update_personaldata(personalData):
    items = jsonTransfer.jsontransform(personalData)
    try:
        print(items['userID'])
    except:
        print("None")
    ref = db.collection(u'cguscholar').document((items['id']))
    ref.collection(u'updateTime').document(
        (items['personalData']['updateTime'])).set(items['cited'])
    ref.set(items['personalData'])

# labellist加入label domain


def add_labeluserIDinfo(item, label):
    items = jsonTransfer.jsontransform(item)
    print(len(items['userID']))
    ref = db.collection(u'Label-Domain').document(label)
    ref.set(items)

# 新增未被爬過的label


def add_labeldomain(label):
    for i in label:
        ref = db.collection(u'Label-Domain').document(i)
        doc = ref.get()
        if not doc.exists:
            ref.set({u'updateTime': None})

# user profile updatetime


def get_userupdatetime(ID):
    users_ref = db.collection(u'cguscholar').document(ID)
    doc = users_ref.get()
    if doc.exists:
        checkTemp = doc.to_dict()
        Timestamp = checkTemp['updateTime']
        return Timestamp
    else:
        return ('Not found')

# v內容為空的labelname


def get_emptylabelname():
    emptylabelname = ''
    while(1):
        try:
            emptylabelname = db.Label_Domain.find_one({"updateTime":  None})
            break
        except:
            continue
    print(emptylabelname)
    return emptylabelname

# v取得最久沒更新的label


def get_labelforCGUScholar():
    label = ''
    while(1):
        try:
            label = db.Label_Domain.find_one(
                {"$query": {}, "$orderby": {"updateTime": 1}})
            break
        except:
            continue
    return label


if __name__ == '__main__':
    A = db.Label_Domain.find_one(
        {"$query": {}, "$orderby": {"updateTime": 1}})
    print(A)
