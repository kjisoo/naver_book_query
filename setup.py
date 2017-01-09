from setuptools import setup

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

setup(
    name="Naver-Book-Query",
    version='0.9.0',
    author='Kim jisoo',
    author_email='kim@jisoo.net',
    license='MIT License',
    url='https://github.com/kjisoo/naver_book_query',
    packages=['naver_book_query'],
    description="Use naver book query like sqlalchemy",
    long_description=readme,
    install_requires=[],
)