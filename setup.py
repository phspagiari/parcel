#!/usr/bin/env python

import os
import sys

import parcel

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [ 'parcel' ]
requires = [ 'fabric>=1.4.3']

setup(
    name='parcel',
    version=parcel.__version__,
    description='Python Webapp Deployment Made Easier.',
    long_description="""Classes to help writing fabric files for python app deployment""",
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
