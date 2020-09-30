# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages


setup(
    name='augmixations',
    version='0.0.2',
    description='Object detection augmentations.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TheDenk/augmixations',
    author='Karachev Denis',
    author_email='komedian@bk.ru',
    license='MIT',
    install_requires=['numpy>=1.8.0'],
    packages=find_packages(),
)
