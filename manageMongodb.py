from distutils.log import error
from itertools import count

import pymongo
from pymongo import MongoClient
import jsonTransfer
cluster = MongoClient(
    "mongodb+srv://CGUScholar:cguscholarpwd@cluster0.bpq9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["CGUScholar"]

collection = db["test"]

# 更新userprofile


# def update_personaldata(personalData):
#     personalDatadict = jsonTransfer.jsontransform(personalData)
#     try:
#         print(personalDatadict['userID'])
#     except:
#         print("None")
#     ref = db.collection(u'cguscholar').document((items['id']))
#     ref.collection(u'updateTime').document(
#         (items['personalData']['updateTime'])).set(items['cited'])
#     ref.set(items['personalData'])

# labellist加入label domain


def add_labeluserIDinfo(item):
    labeldict = jsonTransfer.jsontransform(item)
    print(len(labeldict['userID']))
    db.Label_Domain.update_one({'_id': labeldict['_id']}, {"$set": {"updateTime": labeldict['updateTime']}, "$addToSet": {
        "userID": {"$each": labeldict['userID']}}})

# 新增未被爬過的label


def add_labeldomain(newlabel):
    for label in newlabel:
        labeldict = {"_id": label, "userID": [], "updateTime": None}
        try:
            db.Label_Domain.insert_one(labeldict)
        except error:
            print(error)

# user profile updatetime


def get_userupdatetime(ID):
    try:
        Timestamp = db.cguscholar.find_one({"_id":  ID})
        return Timestamp['personalData']['updateTime']
    except:
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
    print(type(emptylabelname['_id']))
    return emptylabelname['_id']

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
    return label['_id']


if __name__ == '__main__':

    newlabel = ['Machine Learning', 'Causal Inference',
                'Artificial Intelligence', 'Computational Photography', 'Statistics']
    for label in newlabel:
        labeldict = {"_id": label, "userID": [], "updateTime": None}
        try:
            db.Label_Domain.insert_one(labeldict)
        except error:
            print(error)
