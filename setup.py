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
requires = [ 'fabric>=1.4.3', 'requests']

setup(
    name='parcel',
    version=parcel.__version__,
    description='Python Webapp Deployment Made Easier.',
    long_description=open('README.txt').read(),
    author='Crispin Wellington',
    author_email='retrogradeorbit@gmail.com',
    url='https://bitbucket.org/andrewmacgregor/parcel',
    packages=packages,
    package_data={'': ['LICENSE']},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    )
)
