up-main:
	docker network create --driver=bridge --subnet=172.20.0.0/16 blog && \
	docker compose -f users/docker-compose-main.yml up -d && \
	docker compose -f blog/docker-compose-main.yml up -d && \
	docker compose -f api_gateway/docker-compose-main.yml up -d

down-main:
	docker compose -f users/docker-compose-main.yml down && \
	docker compose -f blog/docker-compose-main.yml down && \
	docker compose -f api_gateway/docker-compose-main.yml down && \
	docker network prune --force

reload-main:
	docker compose -f users/docker-compose-main.yml up --build --detach -d && \
	docker compose -f blog/docker-compose-main.yml up --build --detach -d && \
	docker compose -f api_gateway/docker-compose-main.yml up --build --detach
	
