#!/usr/bin/env python
from setuptools import setup

requires = [
    'gevent==0.13.7',
    'Flask==0.8',
]

setup(
    name='Mini Triage',
    version='1.0',
    description='A prototype app that allows user(s) to triage events into various categories.',
    author='Greg Reinbach',
    author_email='greg@reinbach.com',
    url='https://github.com/reinbach/mini-triage',
    install_requires=requires,
)