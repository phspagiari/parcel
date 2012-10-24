Tutorials
=========

Heres some step by step tutorials of deploying small example projects in popular python web frameworks.

Django
------

Setting Up The Project
^^^^^^^^^^^^^^^^^^^^^^

Start with an empty directory. Make a `requirements.txt` file and put the following in it::

    django==1.4.2
    
Let's build a virtual python for our development::

    $ virtualenv vp
    $ vp/bin/pip install -r requirements.txt
    
This should download and install django locally. Let's activate our virtual python and start a django project::

    $ source vp/bin/activate
    $ django-admin.py startproject myproject
    
Let's change into the project directory and fire up the development web server::

    $ cd myproject/
    $ python manage.py runserver

Point your browser at http://localhost:8000/ and see the django splash page.

Writing The Fabfile
^^^^^^^^^^^^^^^^^^^

Go back to the project base. That's the directory with the virtual python 'vp' directory one above 'myproject'::

    $ cd ..
    
Make a `fabfile.py` here and put the following in it::

    from parcel.deploy import uWSGI
    from parcel.probes import *
    
    def deb():
        deploy = uWSGI("myproject", base="webapps")
        deploy.prepare_app()
        deploy.add_supervisord_uwsgi_service("mproject",port=10000)
        deploy.build_deb()
        
Fisrt thing is we are using the uWSGI Deployment object. This is a stripped down uwsgi deployment container::

    .. todo:: Talk about different deployment strategies.
        
Let's have a quick look at the options here. The first argument to Deployment is the package name. This will be used to
name the binary package when it's built. The variable `base` is a path on the remote host where the package will be installed to. If this
is ommitted, the install path is the home directory of the building user. If it's an absolute path (starting with /) then
it's installed in that path. If it's a relative path like this setting, it is installed into that path relative to the
build users home directory. So in our case it will be "~/webapps". So, for instance, if we were to build the package as
user apache (pass `-u apache` into our fab call), then the package on debian would be installed under /var/www/webapps.

The prepare_app call copies the code over and setsup the virtual env with the requirements.txt file. Then the add_supervisord_uwsgi_service
sets the package to make a uwsgi daemon start under supervisord. This daemon will listen for web requests on port 10000 and the
supervisor service is called 'myproject'. The final line builds the deb.

Go ahead and build the package::

    $ fab -H debian deb
    
You'll notice as the files were copied, the list of copied files is listed in blue. In this list you will see that copied across
and build into the package is some files in your directory you don't want in there. Firstly, you don't want any local virtualenv being
copied over, as the package builds its own on the destination target. You also don't want your fabfile copied over. Once you build the
deb, if you run the build again, `the deb file you just created would be copied over`! So lets ignore these by listing their globs
in a file called `.rsync-ignore`. You also want to ignore this file. Edit `.rsync-ignore` and put in it the following::

    vp
    *.deb
    fabfile*
    .rsync-ignore
    
Now build the deb again an notice that these files are excluded from the copy::
    
    $ fab -H debian deb
    
Once it's built, you can have a look at directory structure::

    $ fab -H debian deb_tree:myproject_0.0.0_all.deb
    
and more interestingly it's control files::

    $ fab -H debian deb_control:myproject_0.0.0_all.deb
    
Now its time to test if it installs ok. Install the package on the build host as root::

    $ fab -H debian -u root deb_install:myproject_0.0.0_all.deb 
    
Now point your browser at http://debian:10000/ (where debian is the hostname/ip where you installed the deb package) and you should see
exactly what you saw from runserver locally. Congratulations! You just packaged and deployed a django appliaction.

