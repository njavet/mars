run:
	poetry run mars

eval:
	poetry run eval

update:
	poetry version patch
	poetry run python scripts/inject_version.py
	git add .
	git commit -m "new version"

test:
	poetry run pytest


pdf:
	pdflatex thesis/main
	biber thesis/main
	pdflatex thesis/main
	pdflatex thesis/main
