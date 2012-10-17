.. _install:

Installation
============

This document covers the installation of Tailor.

    
Get the Source
--------------

Tailor is available on BitBucket.

Clone the public repository::

    $ hg clone https://bitbucket.org/retrogradeorbit/tailor
    
Once you have a copy of the source code, install it into your python environment::

    $ cd tailor
    $ python setup.py install
    
Check that tailor is successfully installed::

    $ python
    Python 2.6.1 (r261:67515, Jun 24 2010, 21:47:49) 
    [GCC 4.2.1] on debian
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import tailor
