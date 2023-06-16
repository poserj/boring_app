from difflib import SequenceMatcher
from typing import List, Union

import requests
import yaml

from models import ParametrActivity


def get_activity(args) -> str:
    '''сетевой запрос'''
    response = requests.get(args[1] + args[0])
    if response.status_code == 200:
        return response.content
    else:
        raise 'Cant find web-page'

def input_parametr(
    base_accessibility: float, base_type: str, base_participants: int, base_price: float
) -> ParametrActivity:
    '''Запрашиваем предпочтения пользователя'''
    accessibility: float = float(input("accessibility ") or base_accessibility)
    type: str = input("type ") or base_type
    participants: int = int(input("participants ") or base_participants)
    price: float = float(input("price ") or base_price)
    return ParametrActivity(accessibility, type, participants, price)

def form_query(p: ParametrActivity) -> tuple[str, str, str, str]:
    '''формируем параметры get-запроса'''
    return (
        f'participants={p.participants}',
        f'price={p.price}',
        f'accessibility={p.accessibility}',
        f'type={p.type}',
    )


def get_similar(*args) -> List[Union[float, dict]]:
    for a, b, c in args:
        return [SequenceMatcher(None, a, b, autojunk=True).ratio(), c]


def show_result(r: List[Union[float, dict]], max_row: int = 10) -> None:
    r = r[0:max_row]
    for num, i in enumerate(r):
        print(num + 1, i[1]['activity'])


def app_init():
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data
        except yaml.YAMLError as exc:
            print(exc)

