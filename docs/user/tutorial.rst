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

    from parcel.deploy import Deployment
    
    def deb():
        deploy = Deployment("myproject", path="myproject", base="webapps")
        deploy.prepare_app()
        deploy.build_deb()
        
Let's have a quick look at the options here. The first argument to Deployment is the package name. This will be used to
name the binary package when it's built. The `path` option is the path relative to the fabfile of what you want packaged.
By default it is set to ".", but here we want to package the contents of the django project we've made, which is stored
in directory "myproject". 

The variable `base` is a path on the remote host where the package will be installed to. If this
is ommitted, the install path is the home directory of the building user. If it's an absolute path (starting with /) then
it's installed in that path. If it's a relative path like this setting, it is installed into that path relative to the
build users home directory. So in our case it will be "~/webapps". So, for instance, if we were to build the package as
user apache (pass `-u apache` into our fab call), then the package on debian would be installed under /var/www/webapps.


