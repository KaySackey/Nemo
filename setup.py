"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import sys
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

VERSION='0.9.2'

setup(
    name='Nemo Templates',
    version=VERSION,
    description='Lightweight Templating Language',
    long_description=long_description,
    author='Kay Sackey',
    author_email='kay@9cloud.us',
    url='https://github.com/9cloud/Nemo',
    packages=["nemo"],
    requires=["mako (>=0.7.0)", "pyparsing (==1.5.6)", "docopt"],
    license='BSD',
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
    entry_points={
        'console_scripts': [
            'nemo = nemo.__main__:main'
        ],
    },
)
