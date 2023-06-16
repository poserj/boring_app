import json
from difflib import SequenceMatcher
from http import HTTPStatus
from typing import List, Union

import requests
import yaml

from models import ParametrActivity


def get_activity(args) -> str:
    '''сетевой запрос'''
    response = requests.get(args[1] + args[0])
    if response.status_code == 200:
        return response.content


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


def get_similar(*args) -> dict:
    for a, b, c in args:
        # return [SequenceMatcher(None, a, b, autojunk=True).ratio(), c]
        return {
            'matcher': SequenceMatcher(None, a, b, autojunk=True).ratio(),
            'activity': c,
        }


def show_result(r: dict, max_row: int = 10) -> None:
    r = r[0:max_row]
    for num, i in enumerate(r):
        print(num + 1, i['activity']['activity'])


def app_init():
    '''считываем конфиг из config.yaml'''
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data
        except yaml.YAMLError as exc:
            raise yaml.YAMLError


def filter(dicts) -> list:
    '''фильтрует ответы, содержащие ошибки'''
    tmp = []
    for d in dicts:
        d = json.loads(d)
        if d.get('error'):
            continue
        else:
            tmp.append(d)
    return tmp
