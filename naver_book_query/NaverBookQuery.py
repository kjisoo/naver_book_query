import copy
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
        self.__offset = 1
        self.__limit = 10
        self.criterion = {}

    @generative
    def filter(self, *criterion):
        self.criterion = {key: value for dic in criterion for key, value in dic.items()}

    @generative
    def offset(self, offset):
        self.__offset = offset + 1

    @generative
    def limit(self, limit):
        self.__limit = limit

    def count(self):
        pass

    def get(self, isbn):
        self.criterion['isbn'] = isbn
        self.offset(0)
        self.limit(1)
        return self.__request()

    def first(self):
        self.__limit = 1
        return self.__request()

    def all(self):
        return self.__request()

    def __request(self):
        if self.client_key is None or self.secret_key is None:
            raise EnvironmentError('Undefined client_key or secret_key')
        headers = {
            'X-Naver-Client-Id': self.client_key,
            'X-Naver-Client-Secret': self.secret_key,
        }
        request = urllib.request.Request(self.__base_url + self.__get_param(),
                                         headers=headers)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as error:
            pass
        return response.read().decode('utf-8')

    def __get_param(self):
        rename_table = {
            'query': 'query',
            'offset': 'start',
            'limit': 'display',
            'title': 'd_titl',
            'author': 'd_auth',
            'content': 'd_cont',
            'isbn': 'd_isbn',
            'publisher': 'd_publ',
            'publish_start': 'd_dafr',
            'publish_end': 'd_dato',
        }
        self.criterion['offset'] = self.__offset
        self.criterion['limit'] = self.__limit
        naver_keyword = {}
        for k in self.criterion.keys():
            naver_keyword[rename_table[k]] = self.criterion[k]
        return urllib.parse.urlencode(naver_keyword)
