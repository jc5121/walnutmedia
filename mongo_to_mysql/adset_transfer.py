# -*- coding=UTF-8 -*-

from config import db_mongo, db_mysql


cursor = db_mysql.cursor()


def update_sql(date, platform, adset_id, adset_name, campaign_id, campaign_name, days, retained_users, paying_users, revenue, revenue_events, update_time):
    sql = """
        REPLACE INTO 
        t_adjust_adset(date,platform,adset_id,adset_name,campaign_id,campaign_name,days,retained_users,paying_users,revenue,revenue_events,update_time)
        VALUES('{data}','{platform}','{adset_id}','{adset_name}','{campaign_id}','{campaign_name}',{days},{retained_users},{paying_users},{revenue},{revenue_events},'{update_time}')
    """.format(data=date, platform=platform, adset_id=adset_id, adset_name=adset_name, campaign_id=campaign_id, campaign_name=campaign_name, days=days, retained_users=retained_users,
               paying_users=paying_users, revenue=revenue, revenue_events=revenue_events, update_time=update_time)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db_mysql.commit()
    except:
        # 发生错误时回滚
        db_mysql.rollback()


adsets_dic = dict()


def update_adset(date):

    mongo_query_1 = {'date': date}

    # get max_update_time
    max_update_time = 0
    for platform in db_mongo['adjust_snapshot_ad_1'].find(mongo_query_1):
        if max_update_time < platform['update_time']:
            max_update_time = platform['update_time']

    mongo_query_2 = {
        'date': date,
        'update_time': max_update_time
    }

    # get adset_campaign_id_list
    adset_campaign_id_list = list()
    for campaign in db_mongo['adjust_snapshot_adset_1'].find(mongo_query_2):
        campaign_id = campaign['campaign'].split(' ')[-1][1:-1]
        para_arr = campaign['result_parameters']['trackers']
        for adset in para_arr:
            adset_id_item = adset['name'].split('::')[2].split(' ')[-1]
            if len(adset_id_item) < 9:
                adset_id = "unknown"
            else:
                adset_id = adset_id_item[1:-1]
            adset_campaign_id = (adset_id + campaign_id).encode('utf-8')
            if adset_campaign_id not in adset_campaign_id_list:
                adset_campaign_id_list.append(adset_campaign_id)

    # get adset_dic
    for adset_campaign_id in adset_campaign_id_list:
        adsets_dic[adset_campaign_id] = dict()

    # mergecampaign_name
    for campaign in db_mongo['adjust_snapshot_adset_1'].find(mongo_query_2):
        arr_para = campaign['result_parameters']['trackers']
        arr_set = campaign['result_set']['trackers']
        campaign_id = campaign['campaign'].split(' ')[-1][1:-1]
        campaign_name = campaign['campaign'].split('::')[1].split(' ')[0]
        for i in xrange(len(arr_para)):
            adset = arr_para[i]
            adset_id_item = adset['name'].split('::')[2].split(' ')[-1]
            if len(adset_id_item) < 9:
                adset_id = "unknown"
                platform_name = "Google"
            else:
                adset_id = adset_id_item[1:-1]
                platform_name = "Facebook"
            adset_name = adset['name'].split('::')[-1].replace(adset_id_item, '').strip()
            days = arr_set[i]['periods']
            adset_campaign_id = (adset_id + campaign_id).encode('utf-8')
            for day in days:
                day_int = int(day['period'])
                if day_int not in adsets_dic[adset_campaign_id]:
                    adsets_dic[adset_campaign_id][day_int] = dict()
                    adsets_dic[adset_campaign_id][day_int]['platform'] = platform_name
                    adsets_dic[adset_campaign_id][day_int]['retained_users'] = int(day['kpi_values'][0])
                    adsets_dic[adset_campaign_id][day_int]['paying_users'] = int(day['kpi_values'][1])
                    adsets_dic[adset_campaign_id][day_int]['revenue'] = int(day['kpi_values'][2])
                    adsets_dic[adset_campaign_id][day_int]['revenue_events'] = int(day['kpi_values'][3])
                    adsets_dic[adset_campaign_id][day_int]['campaign_id'] = campaign_id.encode('utf-8')
                    adsets_dic[adset_campaign_id][day_int]['campaign_name'] = campaign_name.encode('utf-8')
                    adsets_dic[adset_campaign_id][day_int]['adset_name'] = adset_name.encode('utf-8')
                    adsets_dic[adset_campaign_id][day_int]['adset_id'] = adset_id.encode('utf-8')
                    adsets_dic[adset_campaign_id][day_int]['days'] = day_int
                else:
                    adsets_dic[adset_campaign_id][day_int]['retained_users'] += int(day['kpi_values'][0])
                    adsets_dic[adset_campaign_id][day_int]['paying_users'] += int(day['kpi_values'][1])
                    adsets_dic[adset_campaign_id][day_int]['revenue'] += int(day['kpi_values'][2])
                    adsets_dic[adset_campaign_id][day_int]['revenue_events'] += int(day['kpi_values'][3])

    for adset_campaign_id in adsets_dic:

        for i in xrange(len(adsets_dic[adset_campaign_id])):
            if i in adsets_dic[adset_campaign_id]:
                print adsets_dic[adset_campaign_id][i]
                days = adsets_dic[adset_campaign_id][i]['days']
                retained_users = adsets_dic[adset_campaign_id][i]['retained_users']
                paying_users = adsets_dic[adset_campaign_id][i]['paying_users']
                revenue = adsets_dic[adset_campaign_id][i]['revenue']
                revenue_events = adsets_dic[adset_campaign_id][i]['revenue_events']
                adset_id = adsets_dic[adset_campaign_id][i]['adset_id']
                adset_name = adsets_dic[adset_campaign_id][i]['adset_name']
                campaign_id = adsets_dic[adset_campaign_id][i]['campaign_id']
                campaign_name = adsets_dic[adset_campaign_id][i]['campaign_name']
                platform = adsets_dic[adset_campaign_id][i]['platform']
                update_sql(date, platform, adset_id, adset_name, campaign_id, campaign_name, days, retained_users, paying_users, revenue, revenue_events,
                           max_update_time)


if __name__ == '__main__':
    update_adset('2018-12-07')