# -*- coding=UTF-8 -*-

from config import db_mongo, db_mysql
import time
from os import path
current_dir = path.dirname(path.abspath(__file__))

cursor = db_mysql.cursor()


# 驼峰命名格式转下划线命名格式
def camel_to_underline(camel_format):
    underline_format = camel_format[0].lower()
    if isinstance(camel_format, str):
        for _s_ in camel_format[1:]:
            underline_format += _s_ if _s_.islower() else '_' + _s_.lower()
    return underline_format


def get_campaign_dic(campaign, update_time):
    campaign_dic = dict()
    campaign_dic['update_time'] = update_time
    campaign_dic['app_id'] = 'cashfrenzy'
    campaign_dic['report_name'] = campaign['reportName']
    campaign_dic['report_type'] = campaign['reportType']
    campaign_dic['date_range_type'] = campaign['dateRangeType']
    campaign_dic['min_date'] = campaign['selector']['dateRange']['min']
    campaign_dic['max_date'] = campaign['selector']['dateRange']['max']

    for k, v in campaign['selector']['fields'].items():
        value = v
        if k == 'Amount':
            value = float(v) / 1000000
        if v[-1] == '%' and (v[0] != '>' or v[0] !='<'):
            value = v[:-1]
        campaign_dic[camel_to_underline(str(k))] = value

    return campaign_dic


def generate_replace_sql(campaign, update_time):

    campaign_dic = get_campaign_dic(campaign, update_time)
    sql = "REPLACE INTO\ngoogle_campaign("
    for k, v in campaign_dic.items():
        sql += (k+',')

    sql = sql[:-1]
    sql += ')\nVALUES('

    for k, v in campaign_dic.items():
        sql += ("'%s'" % v + ',')

    sql = sql[:-1]
    sql += ')'

    return sql


if __name__ == '__main__':
    update_time = time.time()

    '''
    one = db_mongo['google_campaign'].find_one()
    sql = generate_replace_sql(one, update_time)
    with open(path.join(current_dir, 'sqls', 'google_campaign_replace_into.sql'), 'w') as fw:
        fw.write(sql)
    '''
    for item in db_mongo['google_campaign'].find():
        sql = generate_replace_sql(item, update_time)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db_mysql.commit()
        except:
            # 发生错误时回滚
            db_mysql.rollback()