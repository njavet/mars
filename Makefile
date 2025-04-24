run:
	poetry run mars

test:
	poetry run pytest

clean:
	rm sentence.db
	rm index.faiss

