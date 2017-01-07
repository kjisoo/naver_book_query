from unittest import TestCase

from naver_book_query.NaverBookQuery import NaverBookQuery


class TestNaverBookQuery(TestCase):
    def setUp(self):
        import os
        client_key = os.environ.get('client_key', False)
        secret_key = os.environ.get('secret_key', False)
        if client_key and secret_key:
            NaverBookQuery.client_key = client_key
            NaverBookQuery.secret_key = secret_key
        else:
            self.fail('Undefined client_key or secret_key')
        self.query = NaverBookQuery()

    def test_client_key(self):
        self.query.client_key = None
        try:
            self.query.first()
            self.fail()
        except EnvironmentError:
            pass

    def test_secret_key(self):
        self.query.secret_key = None
        try:
            self.query.first()
            self.fail()
        except EnvironmentError:
            pass

    def test_filter(self):
        result = self.query.filter(title='python').offset(0).limit(100).all()
        for item in result:
            if 'python' not in item['title'].lower():
                self.fail(item)

    def test_offset(self):
        try:
            self.query.offset(1000)
            self.fail()
        except ValueError:
            self.assert_(True)
        try:
            self.query.offset(0).offset(909)
        except ValueError as e:
            self.fail(e)

    def test_limit(self):
        try:
            self.query.limit(101)
            self.fail()
        except ValueError:
            self.assert_(True)
        try:
            self.query.limit(100).limit(1)
        except ValueError as e:
            self.fail(e)

    def test_count(self):
        count = self.query.filter(title='python').limit(20).count()
        self.assert_(count == 20)

    def test_get(self):
        result = self.query.get('9788992649681')
        if len(result) != 1:
            self.fail(result)

        result = self.query.offset(1).get('9788992649681')
        if len(result) != 1:
            self.fail(result)

        result = self.query.filter(title='JAISDIO@#*U#').get('9788992649681')
        if len(result) != 0:
            self.fail(result)

    def test_first(self):
        result = self.query.filter(title='python').limit(14).offset(0).first()
        if len(result) != 1:
            self.fail(result)

    def test_all(self):
        query = self.query.filter(title='python').offset(0).limit(14).all()
        if len(query) != 14:
            self.fail()
