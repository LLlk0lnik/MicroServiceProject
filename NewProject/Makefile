.PHONY: help up down restart logs db-shell migrate-up migrate-down migrate-create migrate-history migrate-current clean shell

help:
	@echo "Available commands:"
	@echo "  make up              - Start all Docker containers"
	@echo "  make down            - Stop and remove all Docker containers"
	@echo "  make restart         - Restart all Docker containers"
	@echo "  make logs            - Show Docker container logs"
	@echo "  make db-shell        - Connect to PostgreSQL shell"
	@echo "  make shell           - Activate Poetry virtual environment"
	@echo "  make migrate-up      - Apply all pending migrations"
	@echo "  make migrate-down    - Rollback last migration"
	@echo "  make migrate-create  - Create new migration (use MSG='description')"
	@echo "  make migrate-history - Show migration history"
	@echo "  make migrate-current - Show current migration version"
	@echo "  make clean           - Stop containers and remove volumes"

up:
	docker-compose up -d
	@echo "Waiting for database to be ready..."
	@sleep 5
	@echo "Containers started successfully"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

db-shell:
	docker exec -it newproject_postgres psql -U postgres -d postgres

migrate-up:
	poetry run alembic upgrade head

migrate-down:
	poetry run alembic downgrade -1

migrate-create:
	@if [ -z "$(MSG)" ]; then \
		echo "Error: Please provide a migration message using MSG='your message'"; \
		echo "Example: make migrate-create MSG='add users table'"; \
		exit 1; \
	fi
	poetry run alembic revision --autogenerate -m "$(MSG)"

migrate-history:
	poetry run alembic history --verbose

migrate-current:
	poetry run alembic current

clean:
	docker-compose down -v
	@echo "Containers and volumes removed"

shell:
	@echo "To activate Poetry virtual environment, run:"
	@echo "  eval \$$(poetry env activate)"
