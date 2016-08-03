import os

from setuptools import setup, find_packages

__author__ = 'Alejandro F. Carrera'


def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(
    name='TBADDownloader',
    author="Alejandro F. Carrera",
    author_email="alej4fc@gmail.com",
    description="A collector for TuBarrioAlDetalle Web App",
    license="MIT",
    keywords="collector datathon madrid",
    install_requires=['requests']
)