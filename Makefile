run:
	poetry run mars

eval:
	poetry run eval

ce:
	rm frontend/public/results/*
	poetry run eval

update:
	poetry version patch
	poetry run python scripts/inject_version.py
	git add .
	git commit -m "new version"

test:
	poetry run pytest

clean:
	rm sentence.db
	rm index.faiss

