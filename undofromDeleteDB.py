import time
import getTime
import pymongo
from pymongo import MongoClient
import manageMongodb
# cluster = MongoClient(
# "mongodb+srv://CGUScholar:cguscholarpwd@cluster0.bpq9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
cluster = MongoClient("mongodb://localhost:27017/")
#origindb = cluster["CGUScholar_com"]
#db = cluster["DeleteData"]
db = cluster["CGUScholar_com"]
origindb = cluster["DeleteData"]

def movetodeleteDB(collection,ID):
    while db[collection].count_documents({'_id': ID}, limit=1) == 0:
        try:            
            profiledata = origindb[collection].find_one({"_id": ID})
            profiledata['updateTime'] = getTime.currentTime()                
            db[collection].insert_one(profiledata)
                
        except:
            manageMongodb.mongo_errorcheck()
    print('--undo '+ID+ ' from  (' + collection + ')')
    return True
  
def delete_jsonfileby_id(collection, id):
    try:
        origindb[collection].delete_one({"_id": id})
        print('Delete ' + id + ' from '  +collection)
    except:
        manageMongodb.mongo_errorcheck()

def undofile():
    collection0 = 'cguscholar'
    collection1 = 'articles'
    listfile = list(origindb[collection0].find({'updateTime':{'$gt':'2022-12-06'}}))
    for profile in listfile:
    	ID = profile['_id']

    	movetodeleteDB(collection0,ID)
    	movetodeleteDB(collection1,ID)
    	delete_jsonfileby_id(collection1, ID)
    	delete_jsonfileby_id(collection0, ID)
    	time.sleep(0.01)
undofile()
