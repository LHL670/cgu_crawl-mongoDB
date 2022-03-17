import collections
from pickle import NONE
from turtle import update
from unicodedata import name
import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://CGUScholar:cguscholarpwd@cluster0.bpq9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["test"]

collection = db["test"]
dblst = cluster.list_database_names()
print(dblst)
test = {"_id": 'cZ-fHPAAAJ'}
# post = {"$set": {"name": "test", "updaeTime": "2022-03-14 13:38:00"}}
e = {'_id': 'pZ-fHPAAAJ',
     'personalData': {'name': 'Bernhard Scholkopf',
                      'university': 'None',
                      'picture': 'https://scholar.googleusercontent.com/citations?view_op=view_photo&user=DZ-fHPgAAAAJ&citpid=2',
                      'label': ['Machine Learning',
                                'Causal Inference',
                                'Artificial Intelligence',
                                'Computational Photography',
                                'Statistics']
                      },
     'updateTime': '2021-10-30 00:00:00',
     'cited': {'citations': {'All': '177951', 'Since2016': '80835'},
               'h_index': {'All': '163', 'Since2016': '115'},
               'i10_index': {'All': '577', 'Since2016': '484'}},
     'citedRecord': [{'updateTime': '2021-10-30 00:00:00', 'cited': {'citations': {'All': '177951', 'Since2016': '80835'},
                                                                     'h_index': {'All': '163', 'Since2016': '115'},
                                                                     'i10_index': {'All': '577', 'Since2016': '484'}}}, {'updateTime': '2021-03-14 13:52:05', 'cited': {'citations': {'All': '177951', 'Since2016': '80835'},
                                                                                                                                                                        'h_index': {'All': '163', 'Since2016': '115'},
                                                                                                                                                                        'i10_index': {'All': '577', 'Since2016': '484'}}}]}
newlabel = ['labeltest', 'labeltest2']
# c={"_id":label,"userID":None,"updateTime":None}
a = {"$push": {'citedRecord': {"$each": [{'updateTime': '2022-03-30 15:46:00', 'cited': {'citations': {'All': '177951', 'Since2016': '80835'},
                                                                                         'h_index': {'All': '163', 'Since2016': '115'},
                                                                                         'i10_index': {'All': '577', 'Since2016': '484'}}}]}}}
b = {"$set": {"updateTime": '2022-03-30 15:46:00', 'cited': {'citations': {'All': '171', 'Since2016': '80835'},
                                                             'h_index': {'All': '163', 'Since2016': '115'},
                                                             'i10_index': {'All': '577', 'Since2016': '484'}}}}


def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z


updatedata = merge_two_dicts(a, b)
# {$push:{"citedRecord":{$each:[{'updateTime': '"2022-03-14 15:38:00', 'cited': {'citations': {'All': '177951', 'Since2016': '80835'},
#                                                                                    'h_index': {'All': '163', 'Since2016': '115'},
#                                                                                    'i10_index': {'All': '577', 'Since2016': '484'}}}]}}}

# collection.update_one({"_id": 3}, {"$set": {"name": "sally"}})

# collection.insert_one(e)
db2 = cluster["CGUScholar"]

collection2 = db2["cguscholar"]
# collection2.update_one(test, updatedata)
# k = {'_id': 'testdomain4', 'userID': [
#     '-pz7muUAAAAJ', '-4IO6dcAAAAJ', '-3PESdQAAAAJ'], "updateTime": "2022-03-21 15:31:23"}
# collection2.update_one({'_id': k['_id']}, {"$set": {"updateTime": k['updateTime']}, "$addToSet": {
#                        "userID": {"$each": k['userID']}}})
db3 = cluster["CGUScholar"]

collection3 = db3["cguscholar"]
# collection3.insert_one(e)
test3 = {"_id": 'pZ-fHPAAAJ'}


def ifdocexists(doc):
    if collection3.count_documents({'_id': doc['_id']}, limit=1) != 0:

        print(str(doc['_id'])+" exist")
        a = {"$push": {'citedRecord': {"$each": doc['citedRecord']}}}
        b = {"$set": {'updateTime': doc['updateTime'], 'cited': doc['cited']}}
        ab = merge_two_dicts(a, b)
        print(ab)
        collection3.update_one({'_id': doc['_id']}, ab)
    else:
        print(str(doc['_id'])+" not found")
        collection3.insert_one(e)


ifdocexists(e)


# myclient = pymongo.MongoClient(
#     "mongodb+srv://CGUScholar:cguscholarpwd@cluster0.bpq9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# mydb = myclient["testMongoDB"]
# dblst = myclient.list_database_names()

# if "testMongoDB" in dblst:
#     print("testMongoDB is existed！")
# mycol = mydb["testMongoCol"]
# collst = mydb.list_collection_names()
# if "testMongoCol" in collst:   # testMongoCol 集合是否存在
#     print("testMongoCol is existed！")
#     mytestData = {"name": "Allen", "gender": "male", "address": "苗栗縣苑裡鎮"}
#     x = mycol.insert_one(mytestData)
#     x = mycol.find_one()
# print(x)
