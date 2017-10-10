from setuptools import setup
from codecs import open
from os import path

BASE_DIR = path.abspath(path.dirname(__file__))
with open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_desc = f.read()

setup(
    name='healthysnake',

    version='0.1.0',

    description='A network service utility for monitoring service health',
    long_description=long_desc,

    license='MIT',

    author='Jim Hill',
    author_email='jim@dammitjim.co.uk',

    classifiers=[
        'Programming Language :: Python :: 3',
    ],

    keywords='health check service monitoring network',
    packages=['healthysnake'],
)
