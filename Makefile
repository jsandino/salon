init:
	pip install --upgrade pip && pip install -r requirements.txt

test:
	pytest tests

run:
	python salon.py