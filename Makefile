test:
	python -m pytest -q

scan:
	python -m job_scanner.main

format:
	black job_scanner

lint:
	flake8 job_scanner

coverage:
	pytest --cov=job_scanner
