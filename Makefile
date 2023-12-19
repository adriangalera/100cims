make: clean cims markdown

clean:
	rm -rfv cims.json

venv:
	python3 -m venv .venv

install:
	pip install -r requirements.txt

cims:
	curl -s https://www.feec.cat/wp-content/cron-scripts/ascensos_cims.txt > cims.json

markdown:
	python generate-markdown.py