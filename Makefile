start:
	@nameko run --config nameko.yaml service;

unit_test:
	@python3 test_storage_file_system.py -v