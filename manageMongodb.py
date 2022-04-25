from distutils.log import error
from itertools import count
import checkDataformat
import queue
import pymongo
from pymongo import MongoClient
import jsonTransfer
cluster = MongoClient(
    "mongodb+srv://CGUScholar:cguscholarpwd@cluster0.bpq9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["CGUScholar"]


# 更新userprofile


def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z


def delete_jsonfileby_id(collection, id):
    db[collection].delete_one({"_id": id})


def update_personaldata(personalData):

    personalDatadict = jsonTransfer.jsontransform(personalData)
    if db.cguscholar.count_documents({'_id': personalDatadict['_id']}, limit=1) != 0:

        print(str(personalDatadict['_id'])+" exist")
        a = {"$push": {'citedRecord': {
            "$each": personalDatadict['citedRecord']}}}
        b = {"$set": {
            'updateTime': personalDatadict['updateTime'], 'cited': personalDatadict['cited']}}
        ab = merge_two_dicts(a, b)
        # print(ab)
        db.cguscholar.update_one({'_id': personalDatadict['_id']}, ab)
    else:
        print(str(personalDatadict['_id'])+" not found")
        db.cguscholar.insert_one(personalDatadict)


# labellist加入label domain


def add_labeluserIDinfo(item):
    labeldict = jsonTransfer.jsontransform(item)

    db.Label_Domain.update_one({'_id': labeldict['_id']}, {"$set": {"updateTime": labeldict['updateTime']}, "$addToSet": {
        "userID": {"$each": labeldict['userID']}}})
    print("add_labeluserIDinfo: " +
          labeldict['_id']+' : '+str(len(labeldict['userID'])))

# 新增未被爬過的label


def add_labeldomain(newlabel):
    for label in newlabel:
        if db.Label_Domain.count_documents({'_id': label}, limit=1) == 0:

            labeldict = {"_id": label, "userID": [], "updateTime": None}
            try:
                db.Label_Domain.insert_one(labeldict)
            except error:
                print(error)


def adjust_labelname(labelname):
    delete_jsonfileby_id('Label_Domain',  labelname)
    newlabel = checkDataformat.labelnameformat(labelname)

    if db.Label_Domain.count_documents({'_id': newlabel}, limit=1) == 0:

        labeldict = {"_id": newlabel, "userID": [], "updateTime": None}
        try:
            db.Label_Domain.insert_one(labeldict)
        except error:
            print(error)

# user profile updatetime


def get_userupdatetime(ID):
    try:
        Timestamp = db.cguscholar.find_one({"_id":  ID})
        return Timestamp['updateTime']
    except:
        return ('Not found')


# v內容為空的labelname

def get_emptylabelname():
    emptylabelnameQueue = queue.Queue()
    emptylabelname = ''
    labelcount = 0
    while labelcount < 100:
        try:
            getemptylabelname = db.Label_Domain.find(
                {"updateTime":  None})[labelcount]
            emptylabelname = getemptylabelname['_id']

            if '-' in emptylabelname or ' ' in emptylabelname:
                adjust_labelname(emptylabelname)

            labelcount = labelcount + 1

            emptylabelnameQueue.put(emptylabelname)
        except:
            continue
    # check labelname format

    return emptylabelnameQueue

# v取得最近更新的label


def get_labelforCGUScholar():
    labelname = ''
    while(1):
        try:
            # label has been crawled
            getlabelname = db.Label_Domain.find(
                {"updateTime": {"$ne": None}}).sort("updateTime", -1)[0]
            labelname = getlabelname['_id']
            if len(getlabelname['userID']) == 0:
                adjust_labelname(labelname)
                continue

            # check labelname format
            if '-' in labelname or ' ' in labelname:
                adjust_labelname(labelname)
                continue

            break
        except:
            continue
    return labelname


def get_labelforupdateCGUScholaruserID():
    labelnameQueue = queue.Queue()
    labelcount = 0
    while labelcount < 100:
        try:
            # label has been crawled
            getlabelname = db.Label_Domain.find(
                {"updateTime": {"$ne": None}}).sort("updateTime", 1)[labelcount]
            labelname = getlabelname['_id']

            # check labelname format
            if '-' in labelname or ' ' in labelname:
                adjust_labelname(labelname)
                continue

            labelcount = labelcount + 1

            labelnameQueue.put(labelname)
        except:
            continue
    return labelnameQueue


def get_labeldomainuserIDlist(label):
    label_ref = db.Label_Domain.find_one({'_id': label})
    IDtemp = label_ref['userID']
    return IDtemp


# if __name__ == '__main__':
#     label = 'Statistics'
#     label_ref = db.Label_Domain.find_one({'_id': label})
#     docs = label_ref['userID']
#     print(len(docs))
    # print(docs)
    # IDtemp = docs.to_dict()
    # newlabel = ['Machine Learning', 'Causal Inference',
    #             'Artificial Intelligence', 'Computational Photography', 'Statistics']
    # for label in newlabel:
    #     labeldict = {"_id": label, "userID": [], "updateTime": None}
    #     try:
    #         db.Label_Domain.insert_one(labeldict)
    #     except error:
    #         print(error)
