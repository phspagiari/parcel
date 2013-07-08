#!/usr/bin/env python
import os
import sys

import parcel
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requires = [ 'fabric>=1.4.3', 'requests']


setup(
    name='parcel',
    version=parcel.__version__,
    description='Python Webapp Deployment Made Easier.',
    long_description=open('README.txt').read(),
    author='Crispin Wellington',
    author_email='retrogradeorbit@gmail.com',
    url='https://bitbucket.org/andrewmacgregor/parcel',
    package_data={'': ['LICENSE']},
    packages=find_packages(),
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
