# -*- coding:utf-8 -*-
from config import db_mongo, db_mysql
import re
from os import path
current_dir = path.dirname(path.abspath(__file__))

regex_double = r'(^\d+[.]{0,1}?\d*$)|(^[.]{1}\d+$)'
rd = re.compile(regex_double)


# 使用正则表达式判读是否为整形
def is_decimal(ds):
    return rd.findall(ds)


def get_varchar_type(length=500):
    return "varchar(%d) DEFAULT ''" % length


def get_int_type():
    return "int(10) DEFAULT 0"


def get_double_type():
    return "double(15,8) DEFAULT 0"


def get_json_type():
    return "json DEFAULT NULL"


def short_sql_column_name(col_name):
    if 'app_custom_event' in col_name:
        col_name = col_name.replace('app_custom_event', 'ace')
    if 'cost_per_unique' in col_name:
        col_name = col_name.replace('cost_per_unique', 'cpu')
    if 'cost_per_action' in col_name:
        col_name = col_name.replace('cost_per_action', 'cpa')
    return col_name


def generate_sql_by_value(field_types, level, uniq_colums):
    order_keys = sorted(field_types.keys())
    # create table
    unqs = ', '.join(["`%s`" % x for x in uniq_colums])
    sql_lines = list()
    sql_fields = list()
    header = "CREATE TABLE `google_campaign%s` (" % level
    sql_lines.append(header)
    for k in order_keys:
        sql_fields.append(" `%s` %s" % (k, field_types[k]))
    sql_fields.append(" UNIQUE KEY `idx_unq` (%s)" % unqs)
    sql_lines.append(',\n'.join(sql_fields))
    sql_lines.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
    return '\n'.join(sql_lines)


def parse_all_keys(row):
    excludes = ['account_id', 'campaign_id', 'adset_id', 'ad_id']
    field_types = dict()
    for k, v in row.items():
        if k in excludes:
            field_types[k] = get_varchar_type(length=50)
            continue
        if type(row[k]) in [unicode, str]:
            d = row[k].encode('utf8')
            if is_decimal(d):
                field_types[k] = get_double_type()
            else:
                field_types[k] = get_varchar_type()
            continue
        if type(row[k]) == list:
            for a in row[k]:
                arr_key = a['action_type'].replace('.', '___')
                d = a['value'].encode('utf8')
                field_key = '%s__%s' % (k, arr_key)
                field_key = short_sql_column_name(field_key)
                if is_decimal(d):
                    field_types[field_key] = get_double_type()
                else:
                    field_types[field_key] = get_varchar_type()
    field_types['level'] = get_int_type()
    field_types['update_time'] = get_int_type()
    field_types['date'] = get_varchar_type(length=10)
    return field_types


def generate_campaign_sql():
    field_types = dict()
    for one in db_mongo['google_campaign'].find({}):
        for item in one['data']['data']:
            d = parse_all_keys(item)
            field_types.update(d)
    sql = generate_sql_by_value(field_types, 'campaign', ['date', 'level', 'account_id', 'campaign_id'])
    with open(path.join(current_dir, 'sqls', 'google_campaign_create_table.sql'), 'w') as fw:
        fw.write(sql)

