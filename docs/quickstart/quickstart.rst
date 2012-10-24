.. _quickstart:

Quickstart
==========

.. module:: parcel.models

This page gives a good introduction in how to get started with Parcel. 
This assumes you already have Parcel installed. If you do not,
head over to the :ref:`Installation <install>` section.

First, make sure that:

* Parcel is :ref:`installed <install>`
* Parcel is :ref:`up-to-date <updates>`

Secondly, make sure you have a build host setup that you can use to build some packages.
You could setup a :ref:`Debian machine to be a build host <buildhost>` for this quickstart.

From here we assume that you build host is a debian machine available with the name
`debian.localdomain`. Replace that name where it occurs below with your debian machines hostname
or ip address. Let's get started with some simple examples.

Making a Package
------------------

Making a package is very simple. Begin by going to the base directory of your project and making a file `fabfile.py`.

Then in that file write the following::

    from parcel.deploy import Deployment
    
    def deb():
        deploy = Deployment("myapp")
        deploy.prepare_app()
        deploy.build_deb()
        
Now save the fabfile and at the commandline issue::

    $ fab -H debian.localdomain deb
    
When the build is finished you should have a file `myapp_0.0.0_all.deb`::

    $ ls -l *.deb
    
Package Details
---------------
    
If you want to see what's been put in the package, use the deb_ls target found in parcel.probes. First add the following to `fabfile.py`::

    from parcel.probes import *

Then you can use deb_ls to list the contents of the package::

    $ fab -H debian.localdomain deb_ls:myapp_0.0.0_all.deb
    
You will see that the package consists of all the files in your source directory. This is the simplest form of packaging.
This is not that useful as it is only the files. But from here your fabfile can expand to implement some deployment scenarios.

If you look at the packages control files with::

    $ fab -H debian.localdomain deb_control:myapp_0.0.0_all.deb

you will notice the package we have build contains no pre or post, install or remove scripts. You can also see a filesystem tree
of the final installed package with::
    $ fab -H debian.localdomain deb_tree:myapp_0.0.0_all.deb

