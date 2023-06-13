from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from difflib import SequenceMatcher

from ParametrActivity import ParametrActivity
import requests
import json


def get_activity(url: str, base_url: str = 'http://www.boredapi.com/api/activity/?') -> None:
    '''сетевой запрос'''
    response = requests.get(base_url + url)
    if response.status_code == 200:
        return response.content
    else:
        raise 'Cant find web-page'


def input_parametr() -> ParametrActivity:
    '''Запрашиваем предпочтения пользователя'''
    BASE_ACCESSIBILITY: float = 0.9
    BASE_TYPE: str = 'education'
    BASE_PARTICIPANTS: int = 1
    BASE_PRICE: float = 0.0
    accessibility: float = float(input("accessibility ") or BASE_ACCESSIBILITY)
    type: str = input("type ") or BASE_TYPE
    participants: int = int(input("participants ") or BASE_PARTICIPANTS)
    price: int = int(input("price ") or BASE_PRICE)
    return ParametrActivity(accessibility, type, participants, price)


def form_query(p: ParametrActivity) -> list:
    '''формируем параметры get-запроса'''
    return (f'participants={p.participants}', f'price={p.price}', \
            f'accessibility={p.accessibility}', f'type={p.type}')


def get_similar(*args) -> list:
    for a, b, c in args:
        return [SequenceMatcher(None, a, b, autojunk=True).ratio(), c]


def show_result(r: list, max_row: int=10):
    r = r[0:max_row]
    for num, i in enumerate(r):
        print(num+1, i[1]['activity'])


def show_result_debug(r: list, max_row: int = 10):
    r = r[0:max_row]
    for num, i in enumerate(r):
        print(num + 1, i[1]['activity'], '|debug= ', i)



if __name__ == '__main__':
    n = 20
    p = input_parametr()
    query = form_query(p)
    tmp_res = []
    with ThreadPoolExecutor() as executor:
        net_results = set(executor.map(get_activity, query * 10))
    for r in net_results:
        tmp = json.loads(r)
        tmp_res.append(tmp)
    # prepare args for model
    a = [p.price, p.type, p.accessibility, p.participants]
    args = ((a, [tmp['price'], tmp['type'], tmp['accessibility'], tmp['participants']], \
             tmp) \
            for tmp in tmp_res)
    with ProcessPoolExecutor() as executer:
        results = executer.map(get_similar, args)
    del tmp_res
    r = sorted(results, key=lambda x: x[0], reverse=True)
    show_result(r)

