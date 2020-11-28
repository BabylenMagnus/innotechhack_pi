import requests
import json
import os
import time
from const import *


FIELDS = 'photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_200_orig, photo_400_orig, ' \
         'photo_max_orig, domain, has_mobile, contacts, site, education, universities, schools, followers_count, ' \
         'common_count, occupation, relatives, relation, personal, connections, exports, activities, can_post, ' \
         'can_see_all_posts, can_write_private_message, career'.split(', ')


def get_profile_photos(vk_id, access_token=ACCESS_TOKEN):
    json_img = json.loads(requests.get('http://api.vk.com/method/photos.getProfile',
                                       params={'access_token': access_token,
                                               'owner_id': vk_id,
                                               'v': 5.122}).text)
    return [x['sizes'][-1]['url'] for x in json_img['response']['items']]


def find_similar(q, access_token, sort=0, sex=0, city=None, country=None, has_photo=1):
    json_users = json.loads(requests.get('http://api.vk.com/method/users.search',
                                         params={'access_token': access_token,
                                                 'q': q,
                                                 'sort': sort,
                                                 'v': 5.122,
                                                 'city': city,
                                                 'sex': sex,
                                                 'country': country,
                                                 'has_photo': has_photo}).text)
    return [x['id'] for x in json_users['response']['items'] if x['can_access_closed'] == True]


def get_search_photos(q, access_token=ACCESS_TOKEN, sort=0, sex=0, city=None, country=None, has_photo=1):
    searched_dict = {}
    for x in find_similar(q, access_token, sort, sex, city, country, has_photo):
        try:
            searched_dict[x] = get_profile_photos(x, access_token)
        except Exception:
            time.sleep(1)
            searched_dict[x] = get_profile_photos(x, access_token)
    return searched_dict


def search_and_load_photos(q, access_token=ACCESS_TOKEN, directory=os.curdir, sort=0, sex=0, city=None,
                           country=None, has_photo=1):
    photos_dict = get_search_photos(q, access_token, sort, sex, city, country, has_photo)
    for x in photos_dict.keys():
        try:
            os.mkdir(directory + '/' + str(x))
        except Exception:
            continue
        number = 0
        for photo in photos_dict[x]:
            number += 1
            with open(directory + '/' + str(x) + '/' + str(number) + '.jpg', 'wb') as file:
                file.write(requests.get(photo).content)


def get_users_data(userlist, access_token=ACCESS_TOKEN, fields=FIELDS):
    ans = json.loads(requests.get('http://api.vk.com/method/users.get',
                                  params={'access_token': access_token,
                                          'user_ids': ','.join(userlist),
                                          'fields': ','.join(fields),
                                          'v': 5.122}).text)
    return ans


def get_dataset(user_id, access_token=ACCESS_TOKEN, count=50, order='mobile'):
    ans = json.loads(requests.get('http://api.vk.com/method/friends.get',
                                  params={'access_token': access_token,
                                          'user_id': user_id,
                                          'count': count,
                                          # 'fields': 'city',
                                          'v': 5.122}).text)['response']['items']
    return get_users_data([str(x) for x in ans])['response']
