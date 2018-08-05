start:
	@nameko run --config nameko.yaml service;

tests:
	#@python -m unittest storage_file_system_test
	@python -m unittest discover -s test
	#@python -m unittest -v test.test_storage_aws