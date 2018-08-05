start:
	@nameko run --config nameko.yaml service;

tests:
	@python -m unittest discover -s test