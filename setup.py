#!/usr/bin/env python
from distutils.core import setup

VERSION='0.9.2'

setup(
    name='Nemo Templates',
    version=VERSION,
    description='Lightweight Templating Language',
    long_description="""
Nemo is a light weight templating language built upon Mako Templates, and inspired by Haml.
Haml is a fine language, its success within Ruby came from seamlessly interfacing with the culture and practices of the language. What we need isn't a copy of Haml in Python, but a version of it suited to Pythonic practices.
Nemo is active production in many sites, however the code-base could be improved (for example to have automated testing rather than manual testing).

More documentation follows on the Github Repository.
    """,
    author='Kay Sackey',
    author_email='kay@9cloud.us',
    url='https://github.com/9cloud/Nemo',
    packages=["nemo"],
    requires=["mako (>=0.7.0)", "pyparsing (==1.5.6)"],
    license = 'BSD',
    keywords="django mako templating",
    platforms='OS Independent',
    classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Environment :: Web Environment',
              'Intended Audience :: Developers',
              "License :: OSI Approved :: BSD License",
              "Operating System :: OS Independent",
              "Programming Language :: Python",
              'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Text Processing :: Markup :: HTML',
              ],
)