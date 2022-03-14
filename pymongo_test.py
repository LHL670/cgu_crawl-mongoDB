import collections
import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://CGUScholar:cguscholarpwd@cluster0.bpq9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["test"]

collection = db["test"]
dblst = cluster.list_database_names()
print(dblst)

post = {"_id": 3, "name": "test", "updaeTime": "2022-03-14 13:11:00"}

collection.insert_one(post)

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
