#!/usr/bin/env python

import os
import sys

import tailor

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [ 'tailor' ]
requires = []

setup(
    name='tailor',
    version=requests.__version__,
    description='Python Webapp Deployment Made Easier.',
    long_description="""Classes to help writing fabric files for python app deployment"""
    author='Crispin Wellington',
    author_email='retrogradeorbit@gmail.com',
    url='https://bitbucket.org/retrogradeorbit/tailor',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'requests': 'requests'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
)
