start:
	@nameko run --config nameko.yaml service;

tests:
	#@python3 storage_file_system_test.py -v
	#@python3 storage_aws_test.py -v
	#@python -m unittest storage_file_system_test
	#@python -m unittest discover -s test
	@python -m unittest -v test.test_storage_aws