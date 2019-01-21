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


def insert_adset(date, update_time, account):
    mongo_query = {
        'date': date,
        'update_time': update_time,
        'act': account
    }

    for data_item in table_mongo.find(mongo_query):
        print type(data_item)
        for adset in data_item['data']:
            adset_id = adset['adset']['id'].encode('utf-8')
            adset_name = adset['adset']['name'].encode('utf-8')
            status = adset['adset']['status'].encode('utf-8')
            account_id = adset['adset']['account_id'].encode('utf-8')
            bid_strategy = adset['adset']['bid_strategy'].encode('utf-8')
            effective_status = adset['adset']['effective_status'].encode('utf-8')
            configured_status = adset['adset']['configured_status'].encode('utf-8')
            lifetime_budget = adset['adset']['lifetime_budget'].encode('utf-8')
            budget_remaining = adset['adset']['budget_remaining']
            daily_budget = adset['adset']['daily_budget']
            created_time = adset['adset']['created_time'].encode('utf-8')
            update_time = adset['adset']['updated_time'].encode('utf-8')
            start_time = adset['adset']['start_time'].encode('utf-8')
            #date = adset['adset']['date']
            campaign_id = adset['adset']['campaign']['id'].encode('utf-8')
            campaign_name = adset['adset']['campaign']['name'].encode('utf-8')
            ads = json.dumps(adset['adset']['ads'])

            update_sql(adset_id, adset_name, status, account_id, bid_strategy, effective_status, start_time,
                       configured_status, lifetime_budget, budget_remaining, daily_budget, created_time, update_time,
                       date, campaign_id, campaign_name, ads)


if __name__ == '__main__':
    insert_adset('2018-12-16', 1544933141, '460806754444485')