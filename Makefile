all: test

test:
	@echo "---> running tests using tox"
	@python3 -m tox

pytest:
	@echo "---> running tests directly"
	@py.test --tb=short -v --cov sedeprot test_sedeprot.py

coverage:
	@echo "---> building coverage report"
	@coverage html

publish:
	@echo "---> uploading to PyPI"
	@python3 setup.py register
	@python3 setup.py sdist bdist_wheel upload
	@rm -fr build dist .egg

authors:
	@git log --format="%aN <%aE>" | sort -f | uniq