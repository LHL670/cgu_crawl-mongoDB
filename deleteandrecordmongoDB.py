
import getTime
import pymongo
from pymongo import MongoClient
import manageMongodb
# cluster = MongoClient(
# "mongodb+srv://CGUScholar:cguscholarpwd@cluster0.bpq9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
cluster = MongoClient("mongodb://localhost:27017/")
origindb = cluster["CGUScholar_com"]
db = cluster["DeleteData"]


def movetodeleteDB(collection,ID):
    try:
        if origindb[collection].count_documents({'_id': ID}, limit=1) != 0:
            profiledata = origindb[collection].find_one({"_id": ID})
            profiledata['updateTime'] = getTime.currentTime()                
            db[collection].insert_one(profiledata)
            print('--Move '+ID+ ' to DeleteData' + ' (' + collection + ')')
    except:
        manageMongodb.mongo_errorcheck()
