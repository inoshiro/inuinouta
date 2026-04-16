.PHONY: run test check

MANAGE = python inuinouta/manage.py

run:
	$(MANAGE) runserver

test:
	$(MANAGE) test

check:
	$(MANAGE) check
	$(MANAGE) migrate --check
