.PHONY: run test check install

MANAGE = python inuinouta/manage.py

install:
	pip install -r requirements.txt
	pip install --no-deps dynamic-rest==2.3.0

run:
	$(MANAGE) runserver

test:
	$(MANAGE) test

check:
	$(MANAGE) check
	$(MANAGE) migrate --check
