init:
	python setup.py develop
	pip install -r requirements.txt

tests: test

test:
	nosetests ./tests/*.py

docs:
	cd docs; make dirhtml

egg: build
	python setup.py bdist_egg
        
build:
	python setup.py build
        
install: build
	python setup.py install
        
