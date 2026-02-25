.PHONY: install train run

install:
	pip install -r requirements.txt

train:
	python scripts/train_and_explain.py

run:
	uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
