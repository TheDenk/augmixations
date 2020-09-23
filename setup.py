# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages


setup(
    name='augmixations',
    version='0.0.1a',
    description='Object detection augmentations.',
    long_description=open(os.path.join(os.dirname(__file__), 'README.txt')).read(),
    url='https://github.com/TheDenk/augmixations',
    author='Karachev Denis',
    author_email='komedian@bk.ru',
    license='MIT',
    install_requires=[],
    packages=find_packages(exclude=['tests.*', 'tests']),
)
