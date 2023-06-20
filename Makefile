up-prod:
	docker network create --driver=bridge --subnet=172.20.0.0/16 blog && \
	docker compose -f users/docker-compose-prod.yml up -d && \
	docker compose -f blog/docker-compose-prod.yml up -d && \
	docker compose -f api_gateway/docker-compose-prod.yml up -d

down-prod:
	docker compose -f users/docker-compose-prod.yml down && \
	docker compose -f blog/docker-compose-prod.yml down && \
	docker compose -f api_gateway/docker-compose-prod.yml down && \
	docker network rm blog

reload-prod:
	docker compose -f users/docker-compose-prod.yml up --build --detach -d && \
	docker compose -f blog/docker-compose-prod.yml up --build --detach -d && \
	docker compose -f api_gateway/docker-compose-prod.yml up --build --detach
	
