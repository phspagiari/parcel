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

Making a Build Host
-------------------

Download and install vagrant to help you build some vitual machines. Lets start by asking vagrant to boot up an ubuntu image::

    $ vagrant box add base http://files.vagrantup.com/lucid32.box
    $ vagrant init
    $ vagrant up
    
.. tip::
    If you are running an ssh-agent, add the vagrant key to your chain with::
    
    $ ssh-add ~/.vagrant.d/insecure_private_key
    
    Then you can shell in with::
    
    $ ssh -p 2222 vagrant@localhost
    
.. note::

    It may look like you can just ssh into your new box but it is not actually network 
    visible from the host. But port 2222 on localhost is forwarded to port 22 (ssh) on
    the guest VM.

Making a Package
------------------

Making a package is very simple. Begin by going to the base directory of your project and making a file `fabfile.py`.

Then in that file, import the parcel.deploy.Deployment object::

    from parcel.deploy import Deployment

Now, lets create a deb target for our project::

    def deb():
        deploy = Deployment("myapp")
        deploy.prepare_app()
        deploy.build_deb()
        
Now save the fabfile and at the commandline issue::

    $ fab -H localhost --port=2222 deb
    

