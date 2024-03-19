make: clean cims markdown

clean:
	rm -rfv raw-data/100cims/cims* data/100cims/cims.json raw-data/mendikat/*

venv:
	python3 -m venv .venv

install:
	pip install -r requirements.txt

cims:
	curl -s https://www.feec.cat/wp-content/cron-scripts/ascensos_cims.txt > raw-data/100cims/cims-info.json
	python download-cims.py
	python 100cims.py
	python mendikat.py

markdown:
	python generate-markdown.py