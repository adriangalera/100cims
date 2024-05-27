make: clean download cims cims-in-tracks markdown

clean:
	rm -rfv raw-data/100cims/cims* data/100cims/cims.json raw-data/mendikat/*

venv:
	python3 -m venv .venv

install:
	pip install -r requirements.txt

download:
	curl -s https://www.feec.cat/wp-content/cron-scripts/ascensos_cims.txt > raw-data/100cims/cims-info.json
	PYTHONPATH=.venv ; . .venv/bin/activate && python download-cims.py

cims:
	PYTHONPATH=.venv ; . .venv/bin/activate && python 100cims.py
	PYTHONPATH=.venv ; . .venv/bin/activate && python mendikat.py

cims-in-tracks:
	wget https://raw.githubusercontent.com/adriangalera/leaflet-fogofwar/main/data/tracks.geojson -O raw-data/tracks.geojson
	python find-cims-in-tracks.py

markdown:
	python generate-markdown.py