# =========================
# Docker
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
# Database
# =========================

db:
	docker exec -it realtime-face-emotion-recognition-db-1 psql -U postgres -d ferdb

# =========================
# Cleanup
# =========================

clean:
	docker system prune -f