init:
	python setup.py develop
	pip install -r requirements.txt

test:
	nosetests ./tests/*

lazy:
	nosetests --with-color tests/test_requests.py

simple:
	nosetests tests/test_requests.py

docs:
	cd docs; make dirhtml

egg: build
	python setup.py bdist_egg
        
build:
	python setup.py build
        
install: build
	python setup.py install
        
