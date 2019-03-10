venv: FORCE
	python3 -m venv ~/.venv/ecc
	echo . ~/.venv/ecc/bin/activate > venv

deps: FORCE
	touch venv
	. ./venv && pip3 install -r requirements.txt

test: FORCE
	. ./venv && python -m unittest

clean: FORCE
	find . -name "__pycache__" -exec rm -r {} +
	find . -name "*.pyc" -exec rm {} +

FORCE:
