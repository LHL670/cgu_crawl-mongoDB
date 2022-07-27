from distutils.log import error
import checkDataformat
import getTime
import queue
import pymongo
from pymongo import MongoClient
import jsonTransfer
# cluster = MongoClient(
# "mongodb+srv://CGUScholar:cguscholarpwd@cluster0.bpq9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
cluster = MongoClient("mongodb://localhost:27017/")
db = cluster["CGUScholar_com"]



def mongo_errorcheck():
    try:
        cluster.server_info()

    except Exception as err:
        print(err)
        print(getTime.getTime.currentTime)
    return

# 更新userprofile


def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z


def delete_jsonfileby_id(collection, id):
    try:
        db[collection].delete_one({"_id": id})
    except:
        mongo_errorcheck()


def update_personaldata(personalData):
    try:
        personalDatadict = jsonTransfer.jsontransform(personalData)
        if db.cguscholar.count_documents({'_id': personalDatadict['_id']}, limit=1) != 0:

            print(str(personalDatadict['_id'])+" exist")
            a = {"$push": {'citedRecord': {
                "$each": personalDatadict['citedRecord']}}}
            b = {"$set": {
                'personalData': personalDatadict['personalData'],
                'updateTime': personalDatadict['updateTime'],
                'cited': personalDatadict['cited']}}
            ab = merge_two_dicts(a, b)
            # print(ab)
            db.cguscholar.update_one({'_id': personalDatadict['_id']}, ab)
        else:
            print(str(personalDatadict['_id'])+" not found")
            db.cguscholar.insert_one(personalDatadict)
    except:
        mongo_errorcheck()


# labellist加入label domain


def add_labeluserIDinfo(item):
    try:
        labeldict = jsonTransfer.jsontransform(item)

        db.LabelDomain.update_one({'_id': labeldict['_id']}, {"$set": {"updateTime": labeldict['updateTime']}, "$addToSet": {
            "userID": {"$each": labeldict['userID']}}})
        print("add_labeluserIDinfo: " +
            labeldict['_id']+' : '+str(len(labeldict['userID'])))
    except:
        mongo_errorcheck()

def update_articles(id, articles):
    try:
        articlesdict = {}
        articlesdict['_id'] = id
        articlesdict['Articles'] = articles
        articlesdict['updateTime'] = getTime.currentTime()
        articlesdict = jsonTransfer.jsontransform(articlesdict)

        if db.articles.count_documents({'_id': articlesdict['_id']}, limit=1) != 0:
            for article in articlesdict['Articles']:

                if db.articles.count_documents({'_id': articlesdict['_id'], 'Articles.title': article['title']}, limit=1) != 0:
                    # print(article['cited_by_record'])

                    update_exist_cited_by_record = {
                        "$push": {"Articles.$.cited_by_record": article['cited_by_record'][0]}}
                    db.articles.update_one(
                        {'_id': articlesdict['_id'], 'Articles.title': article['title']}, update_exist_cited_by_record)
                else:
                    update_notexist_cited_by_record = {
                        "$push": {"Articles": article}}
                    db.articles.update_one(
                        {'_id': articlesdict['_id']},  update_notexist_cited_by_record)
            db.articles.update_one({'_id': articlesdict['_id']}, {"$set":{'updateTime':articlesdict['updateTime']}})
            print(str(articlesdict['_id'])+" update into articles collection")
        
        else:
            print(str(articlesdict['_id'])+" not found in articles collection")
            db.articles.insert_one(articlesdict)
    except:
        mongo_errorcheck()
# 新增未被爬過的label


def add_labeldomain(newlabel):
    try:
        for label in newlabel:
            if db.LabelDomain.count_documents({'_id': label}, limit=1) == 0:

                labeldict = {"_id": label, "userID": [], "updateTime": None}
                try:
                    db.LabelDomain.insert_one(labeldict)
                except error:
                    print(error)
    except:
        mongo_errorcheck()

def adjust_labelname(labelname):
    try:
        delete_jsonfileby_id('LabelDomain',  labelname)
        newlabel = checkDataformat.labelnameformat(labelname)

        if db.LabelDomain.count_documents({'_id': newlabel}, limit=1) == 0:

            labeldict = {"_id": newlabel, "userID": [], "updateTime": None}
            try:
                db.LabelDomain.insert_one(labeldict)
            except error:
                print(error)
    except:
        mongo_errorcheck()
# user profile updatetime


def get_userupdatetime(ID,collection):
    try:
        try:
            Timestamp = db[collection].find_one({"_id":  ID})
            return Timestamp['updateTime']
        except:
            return ('Not found')
    except:
        mongo_errorcheck()

# v內容為空的labelname

def get_emptylabelname():
    try:
        emptylabelnameQueue = queue.Queue()
        emptylabelname = ''
        labelcount = 0
        while labelcount < 100:
            try:
                getemptylabelname = db.LabelDomain.find(
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
    except:
        mongo_errorcheck()
# v取得最近更新的label


def get_labelforCGUScholar():
    try:
        labelname = ''
        while(1):
            try:
                # label has been crawled
                getlabelname = db.LabelDomain.find(
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
    except:
        mongo_errorcheck()


def get_labelforupdateCGUScholaruserID():
    try:
        labelnameQueue = queue.Queue()
        labelcount = 0
        while labelcount < 100:
            try:
                # label has been crawled
                getlabelname = db.LabelDomain.find(
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
    except:
        mongo_errorcheck() 

def get_labeldomainuserIDlist(label):
    try:
        label_ref = db.LabelDomain.find_one({'_id': label})
        IDtemp = label_ref['userID']
        return IDtemp
    except:
        mongo_errorcheck()

def get_userIDforarticlesupdate():
    try:
        getuserID = []
        getuserIDtemp = list(db.articles.find({}).sort("updateTime", 1).limit(1000))
        for userID in getuserIDtemp:
            getuserID.append(userID['_id'])
        return getuserID
    except:
        mongo_errorcheck()    