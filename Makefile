init:
	python setup.py develop
	pip install -r requirements.txt

tests: test

test: vptest
	vptest/bin/nosetests ./tests/*.py

vtest: vptest
	vptest/bin/nosetests -v ./tests/*.py

coverage:
	vptest/bin/nosetests --with-coverage --cover-erase --cover-package=parcel --cover-html --cover-branches

docs:
	cd docs; make html

egg: build
	python setup.py bdist_egg

build:
	python setup.py build

install: build
	python setup.py install

vptest:
	virtualenv vptest
	vptest/bin/pip install -r test-requirements.txt

