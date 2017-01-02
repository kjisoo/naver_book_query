import copy

import requests


def generative(f):
    def wrapper(*args, **kwargs):
        copied_object = copy.deepcopy(args[0])
        args = (copied_object, ) + args[1:]
        f(*args, **kwargs)
        return copied_object
    return wrapper


class NaverBookQuery:
    client_key = None
    secret_key = None
    __base_url = 'https://openapi.naver.com/v1/search/book_adv.json?'
    __offset = 1
    __limit = 10
    criterion = []

    def __init__(self, client_key=None, secret_key=None):
        self.client_key = client_key
        self.secret_key = secret_key

    def filter(self, *criterion):
        self.criterion = {key: value for dic in criterion for key, value in dic.items()}

    def offset(self, offset):
        self.__offset = offset + 1

    def limit(self, limit):
        self.__limit = limit

    def count(self):
        pass

    def get(self, isbn):
        pass

    def first(self):
        self.__limit = 1
        return self.__request()

    def all(self):
        return self.__request()

    def __request(self, **kwargs):
        if self.client_key is None or self.secret_key is None:
            raise EnvironmentError('Undefined client_key or secret_key')
        response = requests.get(self.__base_url + 'param')
        if response.status_code != 200:
            raise Exception('tt')
