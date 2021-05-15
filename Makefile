COURSE2_IMAGE ?= course2-work:dev

.EXPORT_ALL_VARIABLES:
.DEFAULT_GOAL := run

docker-build:
	@docker build -t $(COURSE2_IMAGE) .

run: COMPOSE := docker-compose -f compose-dev.yml
run: docker-build
	@$(COMPOSE) up

rund: COMPOSE := docker-compose -f compose-dev.yml
rund:
	@$(COMPOSE) up -d

clean: COMPOSE := docker-compose -f compose-dev.yml
clean:
	@$(COMPOSE) down --remove-orphans --rmi=local

rm: COMPOSE := docker-compose -f compose-dev.yml
rm:
	$(COMPOSE) stop
	$(COMPOSE) rm -f

sh: COMPOSE := docker-compose -f compose-dev.yml
sh:
	@$(COMPOSE) exec web bash
