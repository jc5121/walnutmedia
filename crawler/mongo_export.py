# -*- coding: UTF-8 -*-

from mongo_util import db

col = db['user_info']
user_info_file = open('user_info.txt', 'w')
user_info_file.truncate()

#x = col.find_one()
#print str(x['name']) +'|' + str(x['gender'])+ str(x['location']) + str(x['hometown'])


arr = list()
for x in col.find():
    if x['location'] != '' or x['hometown'] != '':
        #user_info = str(x['name']) + '|' + str(x['gender']) + '|' + str(x['location']) + str(x['hometown'])
        user_info = x['name'] + '|' + x['gender'] + '|' + x['location'] + '|' + x['hometown']
        arr.append(user_info.encode('utf-8'))

user_info_file.write('\n'.join(arr))
user_info_file.close()
