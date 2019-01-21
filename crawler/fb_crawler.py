# -*- coding: UTF-8 -*-
import json
import time
import thread
import requests
from bs4 import BeautifulSoup
from get_dic import get_post, get_comment, get_like_user, get_personal_dic
from mongo_util import db
from fb_config import fans_pages_url_list, pages_id_list, payload, headers


# -------------------------------------------------------------
def get_comment_info(comment_url, post_id, page_id, update_time):
    comment_page_url = "https://m.facebook.com" + comment_url
    response = requests.request("GET", comment_page_url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    comments_div = soup.find('div', {'id': 'add_comment_link_placeholder'}).previous_sibling

    if not comments_div.contents:
        return None
    for comment in comments_div.contents[:-1]:
        comment_user_h3 = comment.find('h3')
        if comment_user_h3 is None:
            more_rul = comments_div.contents[-1].find('a')['href']
            return more_rul
        comment_user_a = comment_user_h3.a
        comment_user_name = comment_user_a.text
        comment_user_url = comment_user_a['href']
        comment_content_div = comment_user_h3.next_sibling
        comment_content = comment_content_div.text
        comment_id = post_id + comment_user_name
        comment_dic = get_comment(comment_id, post_id, page_id, comment_content, update_time, comment_user_name, comment_user_url)
        try:
            # change a table and it works -- _id can't same
            db['comments'].insert_one(comment_dic)
        except Exception:
            print "insert error"


def comment_page_crawler(comment_page_url, post_id, page_id, update_time):
    current_url = comment_page_url
    while current_url is not None:
        current_url = get_comment_info(current_url, post_id, page_id, update_time)


# ---------------------------------------------------------------------
# 辅助函数
def get_likes_page_url(post_like_url):
    like_url = "https://m.facebook.com" + post_like_url
    response = requests.request("GET", like_url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # get like_users_url
    like_users_div = soup.find('div', {'id': 'add_comment_switcher_placeholder'}).next_sibling
    like_users_a = like_users_div.find('a')
    like_users_url = like_users_a['href']
    return like_users_url


def get_personal_info(user_url):
    url = "https://m.facebook.com" + user_url
    name = ''
    gender = ''
    location = ''
    hometown = ''
    response = requests.request("GET", url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    name_strong = soup.find('strong')
    if name_strong is not None:
        name = name_strong.text

    gender_div = soup.find('div', {'id': 'basic-info'})
    if gender_div is not None:
        gender_div2 = gender_div.find('div', {'title': 'Gender'})
        if gender_div2 is not None:
            gender_tr = gender_div2.find('tr')
            if gender_tr is not None:
                gender = gender_tr.contents[1].text

    living_div = soup.find('div', {'id': 'living'})
    if living_div is not None:

        location_div = living_div.contents[0].contents[1].contents[0]
        if location_div is not None:
            location = location_div.find('a').text

        hometown_div = location_div.next_sibling
        if hometown_div is not None:
            hometown = hometown_div.find('a').text

    person_dic = get_personal_dic(name, gender, location, hometown)
    try:
        db['user_info'].insert_one(person_dic)
    except Exception:
        print "insert error"


def get_users_info(like_users_url, post_id, page_id, update_time):
    # get user's information
    users_url = "https://m.facebook.com" + like_users_url
    response = requests.request("GET", users_url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    users_li = soup.find_all('li')

    if not users_li:
        return None

    for user_li in users_li[:-1]:
        user_a = user_li.find('a')
        user_name = user_a.text
        user_url = user_a['href']
        get_personal_info(user_url)

        #get_personal_info(user_url)


        #like_id = post_id + user_name
        #like_user_dic = get_like_user(like_id, page_id,
                                      #post_id, update_time, user_name, user_url)
        #try:
            # change a table and it works -- _id can't same
            #db['like_users_merge'].insert_one(like_user_dic)
        #except Exception:
            #print "insert error"

    more_rul = users_li[-1].find('a')['href']
    return more_rul


def like_users_page_crawler(users_page_url, post_id, page_id, update_time):
    current_url = users_page_url
    while current_url is not None:
        current_url = get_users_info(current_url, post_id, page_id, update_time)


# --------------------------------------------------------------
def get_posts_page(fans_page_url, page_id, update_time):
    # 发起请求，获得page
    response = requests.request("GET", fans_page_url, data=payload, headers=headers)

    # 保存到本地文件，方便读取，为啥，不是必须啊
    html_file = open('luckyday_page.html', 'w+', )
    html_file.write(response.text.encode('utf-8'))
    html_file.close()
    # print type(response) -> response obj
    # print type(response.text) -> xml

    # 解析page, 使用lxml解析器
    # soup = BeautifulSoup(open('luckyday_page.html'), 'lxml')
    soup = BeautifulSoup(response.text, 'lxml')
    # print soup.prettify()  # 格式化打印

    # 得到每个post(一条动态)，通过查看page元素
    posts = soup.find_all('div', {'role': 'article'})

    for post in posts:
        print 'post begin:'
        # data
        data = json.loads(post['data-ft'])
        # post_id
        post_id = data['top_level_post_id']

        # content
        content = ''
        content_div = post.contents[0].contents[1]
        if content_div is None:
            print 'error'
            break
        p_s = content_div.find_all('p')
        for p in p_s:
            content += p.text

        bottom_div = post.contents[1].contents[1]
        bottom_a_s = bottom_div.find_all('a')
        # like
        like_a = bottom_a_s[0]
        like_url = like_a['href']
        users_page_url = get_likes_page_url(like_url)
        # *************************调用like_user
        # get_users_info(users_page_url, post_id, page_id, update_time)
        print "like begin:"
        like_users_page_crawler(users_page_url, post_id, page_id, update_time)
        print "like finish."

        # comment
        #if len(bottom_a_s) == 7:
            #comment_a = bottom_a_s[3]
        #else:
            #comment_a = bottom_a_s[2]
        #comment_url = comment_a['href']
        # get_comment_info(comment_url, post_id, page_id, update_time)
        #print "comment begin:"
        #comment_page_crawler(comment_url, post_id, page_id, update_time)
        #print "comment finish."

        #post_dic = get_post(post_id, page_id, content, update_time, data)
        #try:
            # change a table and it works -- _id can't same
            #db['fb_posts'].insert_one(post_dic)
        #except Exception:
            #print "insert error"

        print "post finish."

    # more link
    container_div = soup.find('div', {'id': 'structured_composer_async_container'})
    more_div = container_div.find_all('div', {'class': 'i'})
    more_url = "https://m.facebook.com" + more_div[0].find('a')['href']
    return more_url


def fans_page_crawler(fans_page_url, page_id, update_time):
    print "start."
    current_url = fans_page_url
    flag = 0
    while current_url is not None and flag < 3:
        current_url = get_posts_page(current_url, page_id, update_time)
        flag += 1
        print flag
    print "finish."
# ------------------------------------------


if __name__ == "__main__":
    # get_personal_info('https://m.facebook.com/marylee.studer.9?refid=46&__xts__%5B0%5D=12.%7B%22unit_id_click_type%22%3A%22graph_search_results_item_tapped%22%2C%22click_type%22%3A%22result%22%2C%22module_id%22%3A4010%2C%22result_id%22%3A100030814142812%2C%22session_id%22%3A%22affaae8f407466c05b1e4490df840144%22%2C%22module_role%22%3A%22ENTITY_USER%22%2C%22unit_id%22%3A%22browse_rl%3A83e997df-ad65-0323-18fd-6e8ae96f551c%22%2C%22browse_result_type%22%3A%22browse_type_user%22%2C%22unit_id_result_id%22%3A100030814142812%2C%22module_result_position%22%3A0%7D')
    operate_time = time.time()
    #get_posts_page(fans_pages_url_list[0], pages_id_list[0], operate_time)
    fans_page_crawler(fans_pages_url_list[3], pages_id_list[3], operate_time)




