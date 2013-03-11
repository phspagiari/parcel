# all the rst source files to build documents with
DOCFILES = docs/api.rst docs/authors.rst docs/buildhost.rst docs/index.rst docs/introduction.rst docs/user/cookbook.rst docs/user/install.rst docs/user/quickstart.rst docs/user/tutorial.rst


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

docs: $(DOCFILES) vpdocs
	. vpdocs/bin/activate; cd docs; make html

egg: build
	python setup.py bdist_egg

build:
	python setup.py build

install: build
	python setup.py install

vptest:
	virtualenv vptest
	vptest/bin/pip install -r test-requirements.txt

vpdocs:
	virtualenv vpdocs
	vpdocs/bin/pip install sphinx==1.1.3
