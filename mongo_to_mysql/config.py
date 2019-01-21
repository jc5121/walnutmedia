# -*- coding:utf-8 -*-
from pymongo import MongoClient
import pymysql

# mysql config
mysql_host = '127.0.0.1'
mysql_port = 3306
mysql_user = 'root'
mysql_pass = 'root'  # now is my password
mysql_db = 'adjust_data'

db_mysql = pymysql.connect(mysql_host, mysql_user, mysql_pass, mysql_db)


# mongo config
mongo_host = "127.0.0.1"
mongo_port = 27017
mongo_user = ""
mongo_pass = ""
mongo_db = "wm_emails"  # "wm_emails"

if mongo_user:
    client = MongoClient("mongodb://%s:%s@%s:%s/?authSource=%s" %
                         (mongo_user, mongo_pass, mongo_host, mongo_port, mongo_db))
else:
    client = MongoClient("mongodb://%s:%s/%s" % (mongo_host, mongo_port, mongo_db))

db_mongo = client[mongo_db]

