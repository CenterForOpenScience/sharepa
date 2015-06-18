from setuptools import setup

VERSION = '0.2.1'

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
    author='Fabian von Feilitzsch',
    author_email='fabian@cos.io',
    url='https://github.com/fabianvf/sharepa',
    download_url='https://github.com/fabianvf/sharepa/tarball/{}'.format(VERSION),
    install_requires=install_reqs
)
