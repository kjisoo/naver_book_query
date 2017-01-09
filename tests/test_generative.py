from unittest import TestCase

from naver_book_query import generative


class MockClass:
    def __init__(self):
        self.string = ''
        self.list = []

    @generative
    def test_generative_string(self, string):
        self.string = string

    @generative
    def test_generative_array(self, item):
        self.list.append(item)


class TestGenerative(TestCase):
    original_object = MockClass()
    generative_object = original_object.test_generative_string('test').test_generative_array('A')

    def test_generative(self):
        self.assert_(isinstance(self.generative_object, MockClass))
        self.assertFalse(self.original_object == self.generative_object, 'Two objects must be different.')

    def test_generative_string(self):
        self.assert_(self.original_object.string == '')
        self.assert_(self.generative_object.string == 'test')

    def test_generative_array(self):
        self.assert_(self.original_object.list == [])
        self.assert_(self.generative_object.list == ['A'])
