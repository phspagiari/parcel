.. _buildhost:

Making a Build Host
===================

Start with a new `fabfile.py` and in it put the following single line::

    from parcel.helpers import *
    
This will bring in a bunch of standard fab targets for helping to setup build hosts. Run a `fab -l` to see the targets::

    $ fab -l
    Available commands:

        copy_ssh_key  This copies the local uses id_rsa.pub and id_dsa.pub keys into the authorized_keys
        setup_debian  Set up the build host for building in a debian way

If your key is not already on the build host, copy it across with copy_ssh_key::

    $ fab -H hostname -u root copy_ssh_key
    
Put in the root password when asked and this will set you up for passwordless ssh root access.

Debian
------

To setup a debian build host, use the setup_debian target::

    $ fab -H hostname -u root setup_debian
    

