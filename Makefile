publish:
	python setup.py sdist
	twine upload dist/*

install-test:
	pip install -r requirements-test.txt

test:
	pytest tests/

lint:
	flake8
