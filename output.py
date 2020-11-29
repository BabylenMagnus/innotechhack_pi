import sys
import pymongo
from const import *
import face_encoding
import numpy as np


client = pymongo.MongoClient(MONGO_URL)
db = client.inno_hack
collection = db['embedding']

url = input()
encoding = face_encoding.get_encod(face_encoding.url_to_img(url))
distance = {}

for people in collection.find({}):
    encodings = []
    test_encod = np.array(people['embedding'])
    distance[people['name']] = face_encoding.distance(encoding, test_encod)


min_dist = 1
similar_people = []

for keys, dist in distance.items():
    if dist < min_dist:
        min_dist = dist
        min_dist_peop = keys

for i in collection.find({'name': min_dist_peop}):
    print(i['name'])
