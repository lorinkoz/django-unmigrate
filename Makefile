# Makefile for django-unmigrate

.PHONY: test
test:
	poetry run dunm_sandbox/manage.py test tests

.PHONY: coverage
coverage:
	poetry run coverage run dunm_sandbox/manage.py test tests

.PHONY: coverage-html
coverage-html:
	poetry run coverage run dunm_sandbox/manage.py test tests && poetry run coverage html

.PHONY: reqs
reqs:
	poetry export --without-hashes --dev --format requirements.txt > requirements.txt
