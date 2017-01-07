import copy
import json
import urllib.error
import urllib.parse
import urllib.request


def generative(f):
    def wrapper(*args, **kwargs):
        self = copy.deepcopy(args[0])
        f(self, *args[1:], **kwargs)
        return self
    return wrapper


class NaverBookQuery:
    client_key = None
    secret_key = None
    __base_url = 'https://openapi.naver.com/v1/search/book_adv.json?'

    def __init__(self):
        self.criterion = {
            'start': 1,
            'display': 10,
        }

    @generative
    def filter(self, **criterion):
        self._filter(**criterion)

    def _filter(self, **criterion):
        rename_table = {
            'query': 'query',
            'title': 'd_titl',
            'author': 'd_auth',
            'content': 'd_cont',
            'isbn': 'd_isbn',
            'publisher': 'd_publ',
            'publish_start': 'd_dafr',
            'publish_end': 'd_dato',
        }
        for key, value in criterion.items():
            if key in rename_table:
                self.criterion[rename_table[key]] = criterion[key]

    def offset(self, offset):
        if offset < 0 or offset > 999:
            raise ValueError('Offset only supports between 0-999.')
        self.criterion['start'] = offset + 1
        return self

    def limit(self, limit):
        if limit < 1 or limit > 100:
            raise ValueError('Limit only supports between 1-100.')
        self.criterion['display'] = limit
        return self

    def count(self):
        return self.__request()['display']

    def get(self, isbn):
        self._filter(isbn=isbn)
        self.offset(0)
        self.limit(1)
        return self.__request()['items']

    def first(self):
        self.limit(1)
        return self.__request()['items']

    def all(self):
        return self.__request()['items']

    def __get_param(self):
        return urllib.parse.urlencode(self.criterion)

    def __request(self):
        if self.client_key is None or self.secret_key is None:
            raise EnvironmentError('Undefined client_key or secret_key')

        headers = {
            'X-Naver-Client-Id': self.client_key,
            'X-Naver-Client-Secret': self.secret_key,
        }
        request = urllib.request.Request(self.__base_url + self.__get_param(),
                                         headers=headers)
        response = urllib.request.urlopen(request)

        return json.loads(response.read().decode('utf-8'))
