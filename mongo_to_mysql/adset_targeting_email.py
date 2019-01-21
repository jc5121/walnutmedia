# -*- coding=UTF-8 -*-
import imp

from config import db_mongo, db_mysql
import traceback
import sys
import json

cursor = db_mysql.cursor()


def update_sql(adset_id, adset_name, status, account_id, bid_strategy, effective_status, start_time, configured_status,
               lifetime_budget, budget_remaining, daily_budget, created_time, update_time, date, campaign_id,
               campaign_name, ads):
    sql = """
        REPLACE INTO 
        adset(adset_id, adset_name, status, account_id, bid_strategy, effective_status, start_time, configured_status, 
               lifetime_budget, budget_remaining, daily_budget, created_time, update_time, date, campaign_id, 
               campaign_name, ads)
        VALUES('{adset_id}','{adset_name}','{status}','{account_id}','{bid_strategy}','{effective_status}','{start_time}',
        '{configured_status}','{lifetime_budget}','{budget_remaining}','{daily_budget}','{created_time}',
        '{update_time}','{date}','{campaign_id}','{campaign_name}','{ads}')
    """.format(adset_id=adset_id, adset_name=adset_name, status=status, account_id=account_id, bid_strategy=bid_strategy,
               effective_status=effective_status, start_time=start_time, configured_status=configured_status,
               lifetime_budget=lifetime_budget, budget_remaining=budget_remaining, daily_budget=daily_budget,
               created_time=created_time,  update_time=update_time, date=date, campaign_id=campaign_id, campaign_name=campaign_name,
               ads=ads)
    print sql
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db_mysql.commit()
    except:
        # 发生错误时回滚
        traceback.print_exc(file=sys.stdout)
        db_mysql.rollback()


table_mongo = db_mongo['fb_snapshot_adset']


def insert_adset_targeting(date, update_time, account):
    mongo_query = {
        'date': date,
        'update_time': update_time,
        'act': account
    }

    for data_item in table_mongo.find(mongo_query):
        print type(data_item)
        for adset in data_item['data']:

            targeting = adset['adset']['targeting']
            print type(targeting['user_os'])


if __name__ == '__main__':
    insert_adset_targeting('2018-12-16', 1544933141, '460806754444485')