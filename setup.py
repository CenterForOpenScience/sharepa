from setuptools import setup

VERSION = '0.3.0.dev0'

install_reqs = [
    'elasticsearch-dsl',
    'requests',
    'pandas'
]
setup(
    name='sharepa',
    packages=['sharepa'],
    version=VERSION,
    description='A library for browsing and analyzing SHARE data',
    author='Center for Open Science',
    author_email='contact@cos.io',
    url='https://github.com/CenterForOpenScience/sharepa',
    download_url='https://github.com/CenterForOpenScience/sharepa/tarball/{}'.format(VERSION),
    install_requires=install_reqs
)
