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


.. module:: parcel.distro

Distro
------

Code specific to different distributions can be found in the :class:`Distro <Distro>` object.

.. autoclass:: Distro
   :inherited-members:


Debian
------

Code specific to the Debian distribution can be found in the :class:`Debian <Debian>` object.

.. autoclass:: Debian
   :inherited-members:

Ubuntu
------

Code specific to the Ubuntu distribution can be found in the :class:`Ubuntu <Ubuntu>` object.

.. autoclass:: Ubuntu
   :inherited-members:

CentOS
------

Code specific to the CentOS distribution can be found in the :class:`Centos <Centos>` object.

.. autoclass:: Centos
   :inherited-members:

Helpers
-------

Various helper functions are available in parcel.helpers

.. module:: parcel.helpers
.. autofunction:: copy_ssh_key
.. autofunction:: setup_debian
.. autofunction:: setup_ubuntu
.. autofunction:: setup_centos

Probes
------

Functions for inspecting built packages are available in parcel.probes

.. module:: parcel.probes
.. autofunction:: deb_ls
.. autofunction:: deb_install
.. autofunction:: deb_control
.. autofunction:: deb_tree
