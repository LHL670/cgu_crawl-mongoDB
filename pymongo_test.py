import collections
import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://CGUScholar:cguscholarpwd@cluster0.bpq9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["test"]

collection = db["test"]
dblst = cluster.list_database_names()
print(dblst)
test = {"_id": 'DZ-fHPAAAJ'}
# post = {"$set": {"name": "test", "updaeTime": "2022-03-14 13:38:00"}}
e = {'_id': 'DZ-fHPAAAJ',
     'personalData': {'name': 'Bernhard Schölkopf',
                      'university': 'None',
                      'picture': 'https://scholar.googleusercontent.com/citations?view_op=view_photo&user=DZ-fHPgAAAAJ&citpid=2',
                      'label': ['Machine Learning',
                                'Causal Inference',
                                'Artificial Intelligence',
                                'Computational Photography',
                                'Statistics'],
                      'updateTime': '2021-10-09 13:52:05'},
     'cited': {'citations': {'All': '177951', 'Since2016': '80835'},
               'h_index': {'All': '163', 'Since2016': '115'},
               'i10_index': {'All': '577', 'Since2016': '484'}},
     'citedRecord': [{'updateTime': '2021-10-09 13:52:05', 'cited': {'citations': {'All': '177951', 'Since2016': '80835'},
                                                                     'h_index': {'All': '163', 'Since2016': '115'},
                                                                     'i10_index': {'All': '577', 'Since2016': '484'}}}, {'updateTime': '2021-03-14 13:52:05', 'cited': {'citations': {'All': '177951', 'Since2016': '80835'},
                                                                                                                                                                        'h_index': {'All': '163', 'Since2016': '115'},
                                                                                                                                                                        'i10_index': {'All': '577', 'Since2016': '484'}}}]}
a = {"$push": {'citedRecord': {"$each": [{'updateTime': '"2022-03-14 15:38:00', 'cited': {'citations': {'All': '177951', 'Since2016': '80835'},
                                                                                          'h_index': {'All': '163', 'Since2016': '115'},
                                                                                          'i10_index': {'All': '577', 'Since2016': '484'}}}]}}}
# {$push:{"citedRecord":{$each:[{'updateTime': '"2022-03-14 15:38:00', 'cited': {'citations': {'All': '177951', 'Since2016': '80835'},
#                                                                                    'h_index': {'All': '163', 'Since2016': '115'},
#                                                                                    'i10_index': {'All': '577', 'Since2016': '484'}}}]}}}
collection.update_one(test, a)

# collection.insert_one(e)

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
