.. _api:

API
===

.. module:: parcel.deploy

This part of the documentation covers the application programming interface of Parcel.

Deployment
-----------

The majority of work done by Parcel is using the :class:`Deployment <Deployment>` object.

.. autoclass:: Deployment
   :inherited-members:

Helpers
-------

Various helper functions are available in parcel.helpers

.. module:: parcel.helpers
.. autofunction:: copy_ssh_key
.. autofunction:: setup_debian
.. autofunction:: setup_ubuntu

Probes
------

Functions for inspecting built packages are available in parcel.probes

.. module:: parcel.probes
.. autofunction:: deb_ls
.. autofunction:: deb_install
.. autofunction:: deb_control
.. autofunction:: deb_tree

Tasks
-----

Some prebuilt functions to use for common tasks or to copy and adapt.

.. module:: parcel.tasks
.. autofunction:: build
.. autofunction:: build_for_uwsgi
