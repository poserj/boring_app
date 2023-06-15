from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from difflib import SequenceMatcher
from ParametrActivity import ParametrActivity
import requests
import json
import yaml


def get_activity(args) -> str:
    '''сетевой запрос'''
    response = requests.get(args[1] + args[0])
    if response.status_code == 200:
        return response.content
    else:
        raise 'Cant find web-page'


def input_parametr(base_accessibility: float, base_type: str,\
                   base_participants: int, base_price: float) -> ParametrActivity:
    '''Запрашиваем предпочтения пользователя'''
    accessibility: float = float(input("accessibility ") or base_accessibility)
    type: str = input("type ") or base_type
    participants: int = int(input("participants ") or base_participants)
    price: float = float(input("price ") or base_price)
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
    with open("config.yaml", "r") as stream:
        try:
            data = (yaml.safe_load(stream))
            api = data['API']
            app = data['APP']
        except yaml.YAMLError as exc:
            print(exc)
    p = input_parametr(app['base_accessibility'], app["base_type"],\
                       app["base_participants"], app["base_price"])
    query = form_query(p)
    tmp_res = []
    args = ((tmp, api['base_url']) for tmp in (query * 10))
    net_results = set()
    with ThreadPoolExecutor() as executor:
        net_results = set(executor.map(get_activity, args))
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

