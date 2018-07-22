start:
	@nameko run --config nameko.yaml service;

unit_test:
	@python3 test_controller.py -v