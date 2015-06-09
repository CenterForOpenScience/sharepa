from setuptools import setup
from pip.download import PipSession
from pip.req import parse_requirements

VERSION = '0.1'

install_reqs = map(
    lambda ir: str(ir.req),
    parse_requirements('requirements.txt', session=PipSession())
)

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
