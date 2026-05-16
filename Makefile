# =========================
# Production
# =========================

up:
	docker compose up --build -d

down:
	docker compose down

restart:
	docker compose down
	docker compose up --build -d

logs:
	docker compose logs -f

ps:
	docker compose ps


# =========================
# Development
# =========================

dev-up:
	docker compose -f docker-compose.dev.yml up --build

dev-down:
	docker compose -f docker-compose.dev.yml down

dev-restart:
	docker compose -f docker-compose.dev.yml down
	docker compose -f docker-compose.dev.yml up --build -d

dev-logs:
	docker compose -f docker-compose.dev.yml logs -f

dev-ps:
	docker compose -f docker-compose.dev.yml ps


# =========================
# Database
# =========================

db:
	docker exec -it fer-db psql -U postgres -d ferdb


# =========================
# Cleanup
# =========================

clean:
	docker system prune -f