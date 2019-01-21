# -*- coding=UTF-8 -*-

from config import db_mongo, db_mysql


cursor = db_mysql.cursor()


# 每个参数出现4次
def update_sql(date, platform, campaign_id, campaign_name, days, retained_users, paying_users, revenue, revenue_events, update_time):
    sql = """
        REPLACE INTO 
        t_adjust_campaign(date,platform,campaign_id,campaign_name,days,retained_users,paying_users,revenue,revenue_events,update_time)
        VALUES('{data}','{platform}','{campaign_id}','{campaign_name}',{days},{retained_users},{paying_users},{revenue},{revenue_events},'{update_time}')
    """.format(data=date, platform=platform, campaign_id=campaign_id, campaign_name=campaign_name, days=days, retained_users=retained_users,
               paying_users=paying_users, revenue=revenue, revenue_events=revenue_events, update_time=update_time)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db_mysql.commit()
    except:
        # 发生错误时回滚
        db_mysql.rollback()


campaigns_dic = dict()


def update_compaign(date):

    mongo_query_1 = {'date': date}

    # get max_update_time
    max_update_time = 0
    for platform in db_mongo['adjust_snapshot_campaign'].find(mongo_query_1):
        if max_update_time < platform['update_time']:
            max_update_time = platform['update_time']

    mongo_query_2 = {
        'date': date,
        'update_time': max_update_time
    }

    # get id_list
    id_list = list()
    for platform in db_mongo['adjust_snapshot_campaign'].find(mongo_query_2):
        para_arr = platform['result_parameters']['trackers']
        for campaign in para_arr:
            campaign_id = campaign['name'].split(' ')[-1][1:-1]
            if campaign_id not in id_list:
                id_list.append(campaign_id)

    # get campaigns_dic
    for id in id_list:
        campaigns_dic[id] = dict()

    # merge
    for platform in db_mongo['adjust_snapshot_campaign'].find(mongo_query_2):
        arr_para = platform['result_parameters']['trackers']
        arr_set = platform['result_set']['trackers']
        for i in xrange(len(arr_para)):
            campaign = arr_para[i]
            campaign_id = campaign['name'].split(' ')[-1][1:-1]
            campaign_name = campaign['name'].split('::')[1].split(' ')[0]
            platform_name = campaign['name'].split('::')[0]
            days = arr_set[i]['periods']
            for day in days:
                day_int = int(day['period'])
                if day_int not in campaigns_dic[campaign_id]:
                    campaigns_dic[campaign_id][day_int] = dict()
                    campaigns_dic[campaign_id][day_int]['platform'] = platform_name.encode('utf-8')
                    campaigns_dic[campaign_id][day_int]['retained_users'] = int(day['kpi_values'][0])
                    campaigns_dic[campaign_id][day_int]['paying_users'] = int(day['kpi_values'][1])
                    campaigns_dic[campaign_id][day_int]['revenue'] = int(day['kpi_values'][2])
                    campaigns_dic[campaign_id][day_int]['revenue_events'] = int(day['kpi_values'][3])
                    campaigns_dic[campaign_id][day_int]['campaign_name'] = campaign_name.encode('utf-8')
                    campaigns_dic[campaign_id][day_int]['campaign_id'] = campaign_id.encode('utf-8')
                    campaigns_dic[campaign_id][day_int]['days'] = day_int
                else:
                    campaigns_dic[campaign_id][day_int]['retained_users'] += int(day['kpi_values'][0])
                    campaigns_dic[campaign_id][day_int]['paying_users'] += int(day['kpi_values'][1])
                    campaigns_dic[campaign_id][day_int]['revenue'] += int(day['kpi_values'][2])
                    campaigns_dic[campaign_id][day_int]['revenue_events'] += int(day['kpi_values'][3])

    for campaign_id in id_list:
        for i in xrange(len(campaigns_dic[campaign_id])):
            if i in campaigns_dic[campaign_id]:
                print campaigns_dic[campaign_id][i]
                days = campaigns_dic[campaign_id][i]['days']
                retained_users = campaigns_dic[campaign_id][i]['retained_users']
                paying_users = campaigns_dic[campaign_id][i]['paying_users']
                revenue = campaigns_dic[campaign_id][i]['revenue']
                revenue_events = campaigns_dic[campaign_id][i]['revenue_events']
                campaign_name = campaigns_dic[campaign_id][i]['campaign_name']
                platform_name = campaigns_dic[campaign_id][i]['platform']
                update_sql(date, platform_name, campaign_id, campaign_name, days, retained_users, paying_users, revenue, revenue_events,
                           max_update_time)


if __name__ == '__main__':
    update_compaign('2018-12-05')