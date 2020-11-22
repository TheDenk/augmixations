# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        file_content = f.read()
    return file_content


def get_version():
    """Get version from the package without actually importing it."""
    init = read('augmixations/__init__.py')
    for line in init.split('\n'):
        if line.startswith('__version__'):
            return eval(line.split('=')[1])


setup(
    name='augmixations',
    version=get_version(),
    description='Object detection augmentations.',
    long_description=read('README.txt'),
    long_description_content_type='text/markdown',
    url='https://github.com/TheDenk/augmixations',
    author='Karachev Denis',
    author_email='komedian@bk.ru',
    license='MIT',
    install_requires=['numpy>=1.11.1'],
    packages=find_packages(),
)
