format: setup ## Lint and static-chec
	isort .
	black --skip-string-normalization .
	mypy main.py
test: setup
	python3 -m unittest
run:
	python3 main.py

setup:
	pip3 install -r requirements.txt


