class Book:
    @classmethod
    def book(cls, data):
        if isinstance(data, dict):
            return Book(data)
        elif isinstance(data, list):
            return [Book(dic) for dic in data]

    def __init__(self, data):
        self.title = data.get('title').replace('<b>', '').replace('</b>', '')
        self.link = data.get('link')
        self.image_link = data.get('image')
        self.author = data.get('author')
        self.price = data.get('price')
        self.discount = data.get('discount')
        self.publisher = data.get('publisher')
        self.publish_date = data.get('pubdate')
        self.isbn = data.get('isbn').split(' ')
        self.description = data.get('description')

