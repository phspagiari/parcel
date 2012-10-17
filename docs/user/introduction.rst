.. _introduction:

Introduction
============

Concepts
--------

Build Host
^^^^^^^^^^

Parcel uses the concept of a *build host* (or hosts) to simplify build procedures. The premise is thus: for each platform you 
want to target for deployment, you have a build host of the same architecture with the same software on it. Fabric connects to 
these machines and issues the build commands. This way the binary package created will be tailored to the final hardware.

These build hosts can be real machines, virtual machines, or cloud instances. It is important that the build hosts mirror
your live deployment environment.

So for example, if your live servers were a mixture of Redhat on 64bit Intel architecture, and Debian on 32bit hardware, then
you would have two build hosts, one Redhat 64bit and one Debian 32bit. You would then build rpms and debs of your project on 
those respective boxes.

The build hosts are specified to fabric via the -H hosts command. For example the following will build two deb packages for
the project for two different platforms::

    $ fab -H debian32.localdomain,debian64.localdomain deb
    
Localhost as Hub
^^^^^^^^^^^^^^^^

Parcel complies to the idea of everything being pushed and pulled from your local machine, the machine in which you have checked
out your source code in and are issuing the `fab` commands from. Everything is pulled to here, and pushed from here. So for instance,
after a .deb is built, it is pulled back to the localhost. When the build host needs a new version of code, the commands are issued
from the local machine, the tree is checked out and updated, and then copied across to the build machine. It is not checked out to
the build machine. When packages are pushed into repositories, it is done from the local machine.

Build From Source, Deploy As Binary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The third concept is to perform all builds from source. Then that source is honed down into a package that is distributed as a
binary. Rather that builds being performed using eggs, or packages, all the source is checked out and a full source build is done.
This ensures complete compatability with the deployment archetecture and system arangement. Once this full source build is done,
the resultant compiled files are packaged into a binary package.

Parcel License
--------------

    .. include:: ../../LICENSE
    
