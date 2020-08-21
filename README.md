# PyQuick


> This is a python app/lib generator that creates a 'empty' python app/lib. And the app/lib 100% uses docker as base for development, test and build.
> Of course, this project itself 100% on docker :D


# Demo

## Generate A New Empty Python App 

![pyquick-demo](https://raw.githubusercontent.com/jevyzhu/pyquick/master/pyquick-demo.gif "pyquick-demo")


# Why PyQuick Created?

## Python's Pain Points

* Python is interpreted language. Using latest python version's feature may make your code not work in environments of old versions.
* Install Python is boring. Linux distrubutions may have different python packages available. For e.g. installatin of python 3.7 on Centos 7 is not convenient. Though pyenv was invented for this but you still need to install pyenv firstly :).
* Python package management slightly sucks. Yes, virtualenv and pipenv are great for isolation. However, some python packages may need conflict binaries, which is not handled by either virtualenv or pipenv.
* Deployment is painful. Target system must have reuqired python version installed. This is not elegant for CI: Jenkins node has to have multiple python versions installed.

## Docker Saves

* Docker can provide nearly system-level isolation.
* No need to install others apart from docker
* Dev/Pod environments keeo consistent - prefect for CI/CD.

## PyQuick Helps

Though this is a super tiny python program but =>

* It gengerates a **start-up python app/lib** for you with Dockerfiles, SetUp Tools, Makefiles, Requirements and others ready.
* The project it generated is 100% **based on Docker**.
* You can immediately start **VSCode to remotely code** your project in container!
* Your **development environment all in code**. Push it to any VCS then you will be able to **restore it** in a few minutes **by one command**.


# Usage

## Run As Docker

The docker image is pretty small - only 40+M.
So it will not take much time for you to pull it.

```bash

# pull docker image

docker pull jingweizhu/pyquick

# generate a new python app in local path: ./myproj

docker run --rm -it -u $(id -u $USER):$(id -g $USER) \
    -v ${PWD}:/tmp/local jingweizhu/pyquick \
    app /tmp/local/myproj

####  OR  ###
# generate a new python lib in local path: ./myproj

docker run --rm -it -u $(id -u $USER):$(id -g $USER) \
    -v ${PWD}:/tmp/local jingweizhu/pyquick \
    lib /tmp/local/myproj

```

## ---- OR ---- 
## Intall From PyPi And Run It

Note: **`python>=3.7`** required

```bash

pip install pyquick

# generate a new python app in ./myproj

pyquick app ./myproj

####  OR  ###
# generate a new python lib in ./myproj

pyquick lib ./myproj


```

## Try Generated Project
You must have:
* docker: ">= 17.06"
* docker-compose: ">= 1.26"
installed

Assume in above you input project name as **`mypy`**

### Make It

```bash
cd ./myproj
make
```
Then check your containers

```bash
docker ps -a
```

A container named `mypy-devenv` should be running.

### Run It (app only)

```bash
cd ./myproj
make run
make run ARGS='-h'
```
Then check your containers

```bash
docker ps -a
```

A container named `mypy-prod` should be running.

### Intall To Local

If have python environment in local machine, 
you can install it:

```bash
cd ./myproj
make install
```

### Build A Python Package

```bash
cd ./myproj
make dist
ls dist/*
```


## Use VSCode To Develop Generated Project 

1. Start VSCode, install Remote extention.
2. Attach to your container : myproj-devenv in VSCode
3. Open terminal. Your project folder attached to container already. Just run
    ```bash
    .vscode/install-vscode-extensions.sh
    ```
4. Reload widdow. Then python extension and other cool extensions available.

## And Even More ...

### Format Codes Of Your Project

```bash
cd ./myproj
make autopep8
```
### Distribute Your Project To PyPi

1. Set up two envs:
```bash
TWINE_USERNAME=<your pypi username>
TWINE_PASSWORD=<your pypi password>
```

2. Run 
```bash
cd ./myproj
make dist-upload
```

# Source code

## Prerequisition
* docker: ">= 17.06"
* docker-compose: ">= 1.26"

## Run Test
```bash
make test
```

## Run
```bash
make docker
make run ARGS="-h"

# creat a new app in your $HOME/myproj
make run ARGS="app /local/myproj"
```

## Install From Code
```bash
make install
```

## Dist
```bash
make dist
```
