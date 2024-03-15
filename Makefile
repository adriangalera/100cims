make: clean cims markdown

clean:
	rm -rfv raw-data/* data/cims.json

venv:
	python3 -m venv .venv

install:
	pip install -r requirements.txt

cims:
	curl -s https://www.feec.cat/wp-content/cron-scripts/ascensos_cims.txt > raw-data/cims-info.json
	python download-cims.py
	python combine-cims.py

markdown:
	python generate-markdown.py