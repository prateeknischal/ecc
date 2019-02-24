venv: FORCE
	python3 -m venv ~/.venv/ecc
	echo . ~/.venv/cloudmarker/bin/activate > venv

deps: FORCE
	touch venv
	. ./venv && pip3 install -r requirements.txt

test: FORCE
	. ./venv && python3 main.py

FORCE:
