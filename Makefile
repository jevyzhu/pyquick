#!/usr/bin/make

PYTHON_VER := 3.7
PROJECT := pyquick
DEV_USER := dev
DEV_CONTAINER := ${PROJECT}-devenv
DEV_SRV := ${PROJECT}-dev-env-srv 

PROD_USER := ops
PROD_SRV := ${PROJECT}-prod-env-srv 

TAG := latest
PROD_IMG := ${PROJECT}-prod:${TAG} 
PROD_IMG_SLIM := ${PROJECT}-prod-slim:${TAG} 

SHELL = /bin/bash

CURRENT_USER_ID := $(shell id -u ${USER}) 
CURRENT_GROUP_ID := $(shell id -g ${USER}) 

.PHONY: clean test dist dist-upload docker-dev docker docker-slim run run-slim autopep8 install

define dev-docker =
	env CURRENT_USER_ID=${CURRENT_USER_ID} \
	CURRENT_GROUP_ID=${CURRENT_GROUP_ID} \
	CURRENT_PROJECT=${PROJECT} \
	DEV_USER=${DEV_USER} \
	PROD_USER=${PROD_USER} \
	PYTHON_VER=${PYTHON_VER} \
	docker-compose up -d --build ${DEV_SRV}
endef

define prod-docker =
	env CURRENT_USER_ID=${CURRENT_USER_ID} \
	CURRENT_GROUP_ID=${CURRENT_GROUP_ID} \
	CURRENT_PROJECT=${PROJECT} \
	DEV_USER=${DEV_USER} \
	PROD_USER=${PROD_USER} \
	PYTHON_VER=${PYTHON_VER} \
	docker-compose up -d --build ${PROD_SRV}
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
		echo &&\
		echo "============ Run In Docker ================" &&\
		echo &&\
		docker run -it --rm -v ${HOME}:/local ${PROD_IMG} $(ARGS) \
	;else \
		python -m ${PROJECT}.main $(ARGS) \
	;fi

run-slim:
	@if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		echo &&\
		echo "============ Run In Docker ================" &&\
		echo &&\
		docker run -it --rm -v ${HOME}:/local ${PROD_IMG_SLIM} $(ARGS) \
	;else \
		python -m ${PROJECT}.main $(ARGS) \
	;fi

dist-upload:
	@if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(dev-docker) > /dev/null &&\
		docker exec -it \
			${DEV_CONTAINER}  \
			twine upload dist/* \
	;else \
		twine upload dist/* \
	;fi

docker-dev:
	$(dev-docker)

docker:
	$(prod-docker)

docker-slim:
	echo -e "1\n" | docker-slim build  ${PROD_IMG} --tag=${PROD_IMG_SLIM} --http-probe=false  --include-path=/usr/local/lib/python${PYTHON_VER}


clean:
	@find . -name '*.py[co]' -delete
	@find . -name '__pycache__' -delete
	@rm -fr dist build *egg*info* coverage* 

autopep8:
	@if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(dev-docker) > /dev/null &&\
		docker exec ${DEV_CONTAINER}  \
		/bin/bash -c "autopep8 --in-place --recursive --aggressive . " \
	;else \
		autopep8 --in-place --recursive --aggressive . \
	;fi

install: test
	python setup.py install --force --user 
