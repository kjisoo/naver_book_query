class Book:
    """
    | The basic type of book model.
    | Implemented __init__ to receive dict.

    dict example

    {
    
        | 'title': 'Title of the book.',
        | 'link': 'hypertext link of the search result document.',
        | 'image': 'The URL of the thumbnail image.',
        | 'author': 'Author of the book',
        | 'price': 'Price of the book',
        | 'discount': 'Discount price of the book',
        | 'publisher': 'Publisher of the book',
        | 'isbn': 'List of isbn separated by spaces.',
        | 'description': 'Summary of the contents of the search result book.',

    }
    """
    def __init__(self, data):
        """

        :param data:
        """
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
