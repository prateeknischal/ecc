venv: FORCE
	python3 -m venv ~/.venv/ecc
	echo . ~/.venv/ecc/bin/activate > venv

deps: FORCE
	touch venv
	. ./venv && pip3 install -r requirements.txt

test: FORCE
	. ./venv && python -m unittest discover -s ecc/tests/

FORCE:
