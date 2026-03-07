install:
	pip install -e .

test:
	pytest

lint:
	flake8 src/ tests/

run:
	uvicorn src.main:app --reload

docker-build:
	docker build -t clinical-validation .

docker-run:
	docker run -p 8000:8000 clinical-validation