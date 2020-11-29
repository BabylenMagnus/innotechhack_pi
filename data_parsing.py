import pandas as pd
import pymongo
from const import *
from face_encoding import get_encod, url_to_img
import vk
from parse_nalog import get_ogrn_inn


translit_map = {
    "а": "a",
    'б': "b",
    "в": "v",
    'г': "g",
    'д': "d",
    'е': "e",
    'ё': "yo",
    'ж': "zh",
    'з': "z",
    'и': "i",
    'й': "j",
    'к': "k",
    'л': "l",
    'м': "m",
    'н': "n",
    'о': "o",
    'п': "p",
    'р': "r",
    'с': "s",
    'т': "t",
    'у': "u",
    'ф': "f",
    'х': "h",
    'ц': "c",
    'ч': "ch",
    'ш': "sh",
    'щ': "sch",
    'ъ': "'",
    'ы': "y",
    'ь': "",
    'э': "e",
    'ю': "ju",
    'я': "ja",
    " ": " "
}

translit = lambda x: ''.join([translit_map[j] for j in x])
vector_to_str = lambda arr: ', '.join(str(x) for x in arr)
vector_to_list = lambda arr: list(float(x) for x in arr)

extremist = pd.read_csv('extremists.csv')


def is_terrorist(name, birh=None):
    data_f = extremist[name == extremist['name']]
    data_s = extremist[name == extremist['second_name']]
    if len(data_f) or len(data_s):
        if birh is not None:
            return len(data_f[data_f['birthday'] == birh]) or len(data_s[data_s['birthday'] == birh])
        return 1
    return 0


client = pymongo.MongoClient(MONGO_URL)
db = client.inno_hack
embedding_db = db['embedding']
vk_db = db['raw_vk']
ohter = db['other']


def clean_data(data):
    new_data = {}
    for keys, value in data.items():
        if value != '':
            new_data[keys] = value
    return new_data


def add_encoding(data):
    full_name = translit((data['first_name'] + ' ' + data['last_name']).lower())
    img = url_to_img(data['photo_max_orig'])
    data = clean_data(data)
    data['name'] = full_name
    a = get_ogrn_inn(data['first_name'] + ' ' + data['last_name'])
    if a is not None:
        ogrn, inn = a
        ohter.insert_one({'name': full_name, 'inn': inn, 'ogrn': ogrn})
    vk_db.insert_one(data)
    try:
        encod = get_encod(img)
        embedding_db.insert_one({'embedding': vector_to_list(encod), 'name': full_name})
    except Exception:
        images = vk.get_profile_photos(data['id'])
        for img in images:
            try:
                img = url_to_img(img)
                encod = get_encod(img)
                embedding_db.insert_one({'embedding': vector_to_list(encod), 'name': full_name})
                break
            except Exception:
                continue


def input_encoder(vk_url):
    test = vk.get_users_data([vk_url.split('/')[-1]])
    add_encoding(test['response'][0])
