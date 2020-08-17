# Python Quick

> This is a python app/lib generator. 
> It 100% uses docker to do: development, test and build.


# Usage 


## Run in docker

```bash

docker pull jingweizhu/pyquick

# generate a new python app on local

docker run --rm -it -u $(id -u $USER):$(id -g $USER) -v <local dir>:/tmp/local jingweizhu/pyquick app /tmp/local/<dir name>

```


## Run as python program

```bash

pip install pyquick

# generate a new python app on local

pyquick app <dir>

```

# Source code
## Prerequisition
* docker: ">= 17.06"
* docker-compose: ">= 1.26"

## Run
```bash
make run
make run ARGS="-h"
```
## Dist
```bash
make dist
```
