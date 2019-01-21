# -*- coding:utf-8 -*-
from pymongo import MongoClient

# mongo config
mongo_host = "127.0.0.1"
mongo_port = 27017
mongo_user = ""
mongo_pass = ""
mongo_db = "wm_emails"  # "wm_emails"

# 使用用户名密码
if mongo_user:
    client = MongoClient("mongodb://%s:%s@%s:%s/?authSource=%s" %
                         (mongo_user, mongo_pass, mongo_host, mongo_port, mongo_db))
else:
    client = MongoClient("mongodb://%s:%s/%s" % (mongo_host, mongo_port, mongo_db))

db_mongo = client[mongo_db]