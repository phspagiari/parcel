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
        
