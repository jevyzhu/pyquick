#!/usr/bin/make
PROJECT := pyquick
DEV_CONTAINER := ${PROJECT}-devenv
DEV_USER := dev
PROD_USER := ops
TAG := latest

SHELL = /bin/bash

CURRENT_USER_ID := $(shell id -u ${USER}) 
CURRENT_GROUP_ID := $(shell id -g ${USER}) 

.PHONY: clean test dist dist-upload docker-dev docker docker-slim run

define dev-docker =
	env CURRENT_USER_ID=${CURRENT_USER_ID} \
	CURRENT_GROUP_ID=${CURRENT_GROUP_ID} \
	CURRENT_PROJECT=${PROJECT} \
	DEV_USER=${DEV_USER} \
	PROD_USER=${PROD_USER} \
	docker-compose up -d --build ${PROJECT}-dev-env-srv
endef

define prod-docker =
	env CURRENT_USER_ID=${CURRENT_USER_ID} \
	CURRENT_GROUP_ID=${CURRENT_GROUP_ID} \
	CURRENT_PROJECT=${PROJECT} \
	DEV_USER=${DEV_USER} \
	PROD_USER=${PROD_USER} \
	docker-compose up -d --build ${PROJECT}-prod-env-srv
endef

dist: clean test
	if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(dev-docker) > /dev/null &&\
		docker exec ${DEV_CONTAINER} \
		/bin/bash -c 'rm -rf dist/* && python setup.py sdist && python setup.py bdist_wheel' \
	;else \
		python setup.py sdist &&\
		python setup.py bdist_wheel \
	;fi

test:
	@if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(dev-docker) > /dev/null &&\
		docker exec ${DEV_CONTAINER} \
		pytest \
			--cov=${PROJECT} \
			--cov-report=term \
			--cov-report=html:coverage-report \
			-v tests \
	;else \
		pytest \
			--cov=${PROJECT} \
			--cov-report=term \
			--cov-report=html:coverage-report \
			-v tests \
	;fi

run:
	@if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(prod-docker) > /dev/null &&\
		echo &&\
		echo "============ Run In Docker ================" &&\
		echo &&\
		docker run ${PROJECT}-prod $(ARGS) \
	;else \
		python -m ${PROJECT}.main \
	;fi

dist-upload:
	@if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(dev-docker) > /dev/null &&\
		docker exec -it ${DEV_CONTAINER}  \
			twine upload dist/* \
	;else \
		twine upload dist/* \
	;fi

docker-dev:
	$(dev-docker)

docker:
	$(prod-docker)

docker-slim:
	docker-slim build  ${PROJECT}-prod:${TAG} --tag=${PROJECT}-prod:${TAG} --http-probe=false  --include-path=/usr/local/lib/python3.8


clean:
	find . -name '*.py[co]' -delete
	rm -fr dist 
	rm -fr build
	rm -fr *egg*info*
	rm -fr coverage*
