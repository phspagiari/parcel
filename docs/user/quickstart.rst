.. _quickstart:

Quickstart
==========

.. module:: parcel.models

This page gives a good introduction in how to get started with Parcel. 
This assumes you already have Requests installed. If you do not,
head over to the :ref:`Installation <install>` section.

First, make sure that:

* Parcel is :ref:`installed <install>`
* Parcel is :ref:`up-to-date <updates>`


Let's get started with some simple examples.


Making a Package
------------------

Making a package is very simple. But before we begin, make a virtual machine with debian
installed on it. Or get access to a debian machine.

Begin by going to the base directory of your project and making a file `fabfile.py`.

Then in that file, import the parcel.deploy.Deployment object::

    from parcel.deploy import Deployment

Now, lets create a deb target for our project::

    def deb():
        deploy = Deployment("myapp")
        deploy.prepare_app()
        deploy.build_deb()
        
Now save the fabfile and at the commandline issue::

    $ fab -H debian.localdomain deb
    

