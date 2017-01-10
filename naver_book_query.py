import copy
import functools
import json
import urllib.error
import urllib.parse
import urllib.request


def generative(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        self = copy.deepcopy(args[0])
        f(self, *args[1:], **kwargs)
        return self
    return wrapper


class NaverBookQuery:
    """Request a query using the api book of Naver.

    Client_key and secret_key are required.

    >>> NaverBookQuery.client_key = 'client key of naver'
    >>> NaverBookQuery.secret_key = 'secret key of naver'

    | The default type for the search is dict.
    | If you want to change the default type, put a value in model_cls.
    | The type must implement __init__ to receive the dict.
    | See :class:`book` for details.
    """
    client_key = None
    secret_key = None
    model_cls = None
    __base_url = 'https://openapi.naver.com/v1/search/book_adv.json?'

    def __init__(self):
        self.criterion = {
            'start': 1,
            'display': 10,
        }
        self.response = None
        self.last_param = None

    @generative
    def filter(self, **criterion):
        """Add to the filter by input criteria.

        example:
            >>> query = NaverBookQuery()

            >>> query = query.filter(title ='title of the book')
            >>> query = query.filter(author = 'me')
            or
            >>> query = query.filter(title='title of the book', author = 'me')

        :param criterion:
            | title : Title of the book
            | author : Author of the book
            | content : Table of Contents
            | isbn : ISBN number of the book
            | publisher : Book publisher
            | publish_start : Publication date of the book
            | publish_end : Publication end date of the book

        :return: Copied object with filter applied
        """
        self._filter(**criterion)

    def _filter(self, **criterion):
        rename_table = {
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
        """offset of search, default 0

        :param offset: Between 0-999
        :return: self with offset applied
        """
        if offset < 0 or offset > 999:
            raise ValueError('Offset only supports between 0-999.')
        self.criterion['start'] = offset + 1
        return self

    def limit(self, limit):
        """display limit of search, default 10

        :param limit: Between 1-100
        :return: self with limit applied
        """
        if limit < 1 or limit > 100:
            raise ValueError('Limit only supports between 1-100.')
        self.criterion['display'] = limit
        return self

    def count(self):
        """Count of search results

        :return: Count of search results
        """
        self.__request()
        return self.response.get('display', 0)

    def get(self, isbn):
        """Search for books by ISBN number.

        Note that filters are applied, except for offset and limit.

        example:
            some book named 'Python' and isbn 10000

            >>> query.get('10000')

            result is book

            >>> query.filter(title='java').get('10000')

            result is None

        :param str isbn: ISBN number of the book
        :return: one object or none, default type is dict
        """
        self._filter(isbn=isbn)
        self.offset(0)
        self.limit(1)
        self.__request()
        return self.__get_item_or_none()

    def first(self):
        """First book in search results
        Note that filters are applied, except for limit.

        :return: one object or none, default type is dict
        """
        self.limit(1)
        self.__request()
        return self.__get_item_or_none()

    def all(self):
        """First book in search results
        Note that filters are applied, except for limit.

        :return: list of object or empty list, default type is list of dict
        """
        self.__request()
        return self.__get_items()

    def __get_item_or_none(self):
        items = self.__get_items()
        if len(items) > 0:
            return items[0]
        return None

    def __get_items(self):
        items = self.response.get('items', [])
        if self.model_cls is not None:
            items = [self.model_cls(item) for item in items]
        return items

    def __get_param(self):
        return urllib.parse.urlencode(self.criterion)

    def __request(self):
        if self.client_key is None or self.secret_key is None:
            raise EnvironmentError('Undefined client_key or secret_key')

        param = self.__get_param()

        if param == self.last_param:
            return
        else:
            self.last_param = param

        headers = {
            'X-Naver-Client-Id': self.client_key,
            'X-Naver-Client-Secret': self.secret_key,
        }
        request = urllib.request.Request(self.__base_url + param,
                                         headers=headers)
        response = urllib.request.urlopen(request).read().decode('utf-8')

        self.response = json.loads(response)
