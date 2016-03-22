#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name='requestbindocker',
    version='1.0.0',
    author='Metalivedev',
    author_email='github@developersupport.net',
    description='HTTP request collector and inspector',
    packages=find_packages(),
    install_requires=['feedparser'],
    data_files=[],
)
