## NaverBookQuery

NaverBookQuery can use Naver's book api as orm query type.  
Need the api key of Naver.  
[NAVER Developers](https://developers.naver.com/main)
### Install
```
pip install naver-book-query
```

### Quickstart
```python
from naver_book_query import Book, NaverBookQuery
NaverBookQuery.client_key = 'client key of naver'
NaverBookQuery.secret_key = 'secret key of naver'

query = NaverBookQuery()
books = query.filter(title='python').all()

books = query.filter(title='python', author='me').all()
#or
books = query.filter(title='python').filter(author='me').all()

books = query.filter(title='python').offset(0).limit(20).all()

book = query.get('0123456789123') # isbn number
```
book is a dict like this  
{  
    'title': 'Title of the book.',  
    'link': 'hypertext link of the search result document.',  
    'image': 'The URL of the thumbnail image.',  
    'author': 'Author of the book',  
    'price': 'Price of the book',  
    'discount': 'Discount price of the book',  
    'publisher': 'Publisher of the book',  
    'isbn': 'List of isbn separated by spaces.',  
    'description': 'Summary of the contents of the search result book.',  
}  
books is list of dict

if you want to get book class
```python
NaverBookQuery.model_cls = Book
books = query.filter(title='python').filter(author='me').all()
book = query.get('0123456789123') # isbn number
```
book is instance of Book class  
books is list of instance of Book class

#### filter criteria
title : Title of the book  
author : Author of the book  
content : Table of Contents  
isbn : ISBN number of the book  
publisher : Book publisher  
publish_start : Publication date of the book  
publish_end : Publication end date of the book  

###### [More documentation(not yet.)](#)
