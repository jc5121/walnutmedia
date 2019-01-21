# -*- coding: UTF-8 -*-
from config import db_mongo
from os import path
current_dir = path.dirname(path.abspath(__file__))


# 判断是否为浮点数
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    return False


# 驼峰命名格式转下划线命名格式
def camel_to_underline(camel_format):
    underline_format = camel_format[0].lower()
    if isinstance(camel_format, str):
        for _s_ in camel_format[1:]:
            underline_format += _s_ if _s_.islower() else '_' + _s_.lower()
    return underline_format


# 确定值类型
def get_value_format(value):
    if is_number(value):
        return "double(20,2) DEFAULT 0"
    elif value[0] == '>' or value[0] == '<':
        return "varchar(100) DEFAULT ''"
    elif value[-1] == '%':
        #value = value[:-1]
        return "double(20,2) DEFAULT 0"
    else:
        return "varchar(100) DEFAULT ''"


def parse_all_keys(row):
    field_types = dict()
    field_types['update_time'] = "varchar(100) DEFAULT ''"
    field_types['app_id'] = "varchar(100) DEFAULT ''"
    field_types['report_name'] = "varchar(100) DEFAULT ''"
    field_types['report_type'] = "varchar(50) DEFAULT ''"
    field_types['date_range_type'] = "varchar(50) DEFAULT ''"
    field_types['min_date'] = "varchar(50) DEFAULT ''"
    field_types['max_date'] = "varchar(50) DEFAULT ''"
    for k, v in row.items():
        field_types[camel_to_underline(str(k))] = get_value_format(v)

    return field_types


def generate_create_sql(field_types, uniq_colums):
    order_keys = sorted(field_types.keys())
    # create table
    unqs = ', '.join(["`%s`" % x for x in uniq_colums])
    sql_lines = list()
    sql_fields = list()
    header = "CREATE TABLE `google_campaign` ("
    sql_lines.append(header)
    for k in order_keys:
        sql_fields.append(" `%s` %s" % (k, field_types[k]))
    sql_fields.append(" UNIQUE KEY `idx_unq` (%s)" % unqs)
    sql_lines.append(',\n'.join(sql_fields))
    sql_lines.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
    return '\n'.join(sql_lines)


if __name__ == '__main__':

    campaign = db_mongo['google_campaign'].find_one()
    fields = campaign['selector']['fields']
    field_types = parse_all_keys(fields)
    uniq_colums = ['app_id', 'campaign_id', 'min_date']
    sql = generate_create_sql(field_types, uniq_colums)
    with open(path.join(current_dir, 'sqls', 'google_campaign_create_table.sql'), 'w') as fw:
        fw.write(sql)

    #print get_value_format('<10%')
