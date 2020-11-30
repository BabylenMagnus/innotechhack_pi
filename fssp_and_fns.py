import requests
from const import ARB_TOKEN, FNS_TOKEN, FSSP_METHODS, FSSP_TOKEN

def arb_dela(q, exact=0, key=ARB_TOKEN):
    arb_req = requests.get('https://damia.ru/api-arb/dela',
                        params={'key':ARB_TOKEN,
                        'q':q,
                        'exact':exact})
    return arb_req.json()


def fns_check(req, key=FNS_TOKEN):
    fns_req = requests.get('https://api-fns.ru/api/check', 
                 params={'key':key,
                         'req':req})
    return fns_req.json()

def fns_egr(req, key=FNS_TOKEN):
    fns_req = requests.get('https://api-fns.ru/api/egr', 
                 params={'key':key,
                         'req':req})
    return fns_req.json()

def fns_bo(req, key=FNS_TOKEN):
    fns_req = requests.get('https://api-fns.ru/api/bo', 
                 params={'key':key,
                         'req':req})
    return fns_req.json()


def get_queries_data(firstname, lastname, region, persontype=0, secondname=None, birthdate=None, fssp_token=FSSP_TOKEN):
    fssp_req = requests.get('https://api-ip.fssp.gov.ru/api/v1.0' + FSSP_METHODS[persontype],
                        params={'token':FSSP_TOKEN,
                                'region': region,
                                'firstname':firstname,
                                'secondname':secondname,
                                'lastname': lastname,
                                'birthdate': birthdate})
    fssp_req_ans = requests.get('https://api-ip.fssp.gov.ru/api/v1.0' + FSSP_METHODS[3],
                            params={'token':FSSP_TOKEN,
                                    'task':fssp_req.json()['response']['task']})
    return fssp_req_ans.json()
    
def closed(req, key=FNS_TOKEN):
    fe = fns_egr(req, key)
    return -3 if fe.json()['items'][0]['ИП']['Статус'] == 'Прекратило деятельность' else 1


def count_problems(req, key=FNS_TOKEN):
    fc = fns_check(req, key)
    return -len(fc.json()['items'])


def count_lawsuits(firstname, lastname, region, persontype=0, secondname=None, birthdate=None, fssp_token=FSSP_TOKEN):
    fssp_ans = get_queries_data(firstname, lastname, region, persontype, secondname, birthdate, FSSP_TOKEN)
    return -len(fssp_ans['response']['result'][0]['result']) if fssp_ans['code'] != 0 else 3
