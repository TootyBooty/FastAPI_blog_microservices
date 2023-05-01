up:
	docker compose -f docker-compose-local.yml up -d

down:
	docker compose -f docker-compose-local.yml down && docker network prune --force

reload:
	docker compose -f docker-compose-local.yml up --build --detach
