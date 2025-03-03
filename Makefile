make: cims markdown

clean:
	rm -rfv raw-data/100cims/cims* data/100cims/cims.json raw-data/mendikat/*

venv:
	python3 -m venv .venv

install:
	PYTHONPATH=.venv ; . .venv/bin/activate && pip install -r requirements.txt

download:
	curl -s https://www.feec.cat/wp-content/cron-scripts/ascensos_cims.txt > raw-data/100cims/cims-info.json
	PYTHONPATH=.venv ; . .venv/bin/activate && python download-cims.py

cims:
	PYTHONPATH=.venv ; . .venv/bin/activate && python 100cims.py
	PYTHONPATH=.venv ; . .venv/bin/activate && python mendikat.py

markdown:
	PYTHONPATH=.venv ; . .venv/bin/activate && python generate-markdown.py