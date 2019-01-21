import hashlib
from lookup_id import get_fb_id


def md5(text):
    return hashlib.md5(text).hexdigest()


def get_post(post_id, page_id, content, update_time, data_ft):
    post_dic = {
        '_id': md5(post_id.encode('utf-8')),
        'page_id': page_id,
        'content': content,
        'update_time': update_time,
        'data': data_ft
    }
    return post_dic


def get_comment(comment_id, page_id, post_id, content, update_time, nickname, link):
    user_code = link.split("?")[0][1:]
    if user_code == 'profile.php':
        return None
    comment_dic = {
        '_id': md5(comment_id.encode('utf-8')),
        'page_id': page_id,
        'post_id': post_id,
        'content': content,
        'update_time': update_time,
        'user': {
            'nickname': nickname,
            'fb_id': get_fb_id(user_code)
        }
    }
    return comment_dic


def get_like_user(like_id, page_id, post_id, update_time, nickname, link):
    user_code = link.split("?")[0][1:]
    if user_code == 'profile.php':
        return None
    like_dic = {
        '_id': md5(like_id.encode('utf-8')),
        'page_id': page_id,
        'post_id': post_id,
        'update_time': update_time,
        'user': {
            'nickname': nickname,
            'link': get_fb_id(user_code)
        }
    }
    return like_dic


def get_personal_dic(name, gender, location, hometown):
    person_dic = {
        'name': name,
        'gender': gender,
        'location': location,
        'hometown': hometown
    }
    return person_dic


if __name__ == "__main__":
    get_fb_id('yummymommy2002')