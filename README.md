# Python Quick

> This is a python app/lib generator that will generate python app/lib that 100% uses docker as base for development, test and build.
> And, the tool itself 100% uses docker for development, test and build.


# Usage


## Run in docker

The docker image is pretty small - only 40+M.
So it will not take much time for you to pull it.

```bash

# pull docker image

docker pull jingweizhu/pyquick

# generate a new python app in local path: ./myproj

docker run --rm -it -u $(id -u $USER):$(id -g $USER) \
    -v ${PWD}:/tmp/local jingweizhu/pyquick \
    app /tmp/local/myproj

```


## Intall from PYPI

```bash

pip install pyquick

# generate a new python app in ./myproj

pyquick app ./myproj

```


# Source code

## Prerequisition
* docker: ">= 17.06"
* docker-compose: ">= 1.26"

## Install from code
```bash
make install
```

## Run
```bash
make run
make run ARGS="-h"
```

## Dist
```bash
make dist
```
