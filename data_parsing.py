import pandas as pd


extremist = pd.read_csv('extremists.csv')


def is_terrorist(name, birh=None):
    data_f = extremist[name == extremist['name']]
    data_s = extremist[name == extremist['second_name']]
    if len(data_f) or len(data_s):
        if birh is not None:
            return len(data_f[data_f['birthday'] == birh]) or  len(data_s[data_s['birthday'] == birh])
        return 1
    return 0
