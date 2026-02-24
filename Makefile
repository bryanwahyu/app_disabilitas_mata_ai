.PHONY: run test lint docker-up docker-down install

install:
	pip install -r requirements.txt

run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest tests/ -v --tb=short

lint:
	ruff check .

lint-fix:
	ruff check --fix .

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
