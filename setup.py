#!/usr/bin/env python
from distutils.core import setup

setup(
    name='Nemo',
    version='0.1',
    description='Lightweight Templating Language',
    author='Kay Sackey',
    author_email='kay@9cloud.us',
    url='http://9cloud.github.com/Nemo/',
    packages=["nemo"],
    requires=["mako (>=0.7.0)", "pyparsing (==1.5.6)"],
)

