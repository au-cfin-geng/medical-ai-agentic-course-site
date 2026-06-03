.PHONY: install serve build validate clean

install:
	pip install -r requirements.txt

serve:
	mkdocs serve

build:
	mkdocs build

validate:
	python scripts/validate_site.py

clean:
	rm -rf site/
