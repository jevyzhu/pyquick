# PyQuick

> This is a python app/lib generator that creates python app/lib. And the app/lib 100% uses docker as base for development, test and build.
> Of course, this project itself 100% on docker :D

# Demo

![pyquick-demo](https://raw.githubusercontent.com/jevyzhu/pyquick/master/pyquick-demo.gif "pyquick-demo")

# Why PyQuick created?

## Python's Pain Points

* Python is interpreted language. Using latest python version's feature can make your code not work in environments of old versions.
* Install Python is boring. Linux distrubutions may have different python packages available. For e.g. installatin of python 3.7 on Centos 7 is not convenient. Though pyenv was invented for this but you still need to install pyenv firstly :).
* Python package management slightly sucks. Yes, virtualenv and pipenv are great for isolation. However, some python packages may need conflict binaries to run, which is not handled by either virtualenv or pipenv.
* Deployment is painful. Target system must have reuqired python version installed. This is not elegant for CI. Jenkins node has to have multiple python versions installed.

## Docker Saves

* Docker can provide nearly system-level isolation.
* No need to install others apart from docker
* Dev/Pod environments keeo consistent - prefect for CI/CD.

## PyQuick Kicks

* It gengerates a minimal  python app/lib for you with Dockerfiles, SetUp Tools, Makefiles, Requirements and others ready.
* The project it generated is 100% based on Docker.
* You can immediately start VSCode to code your project in container!
* Your development environment is completely as code. Push it to any VCS you will never lose your environmnent!


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

```


## Intall From PyPi And Run It

`python>=3.7` required

```bash

pip install pyquick

# generate a new python app in ./myproj

pyquick app ./myproj

```

## Try Your Project!

You must have:

* docker: ">= 17.06"
* docker-compose: ">= 1.26"

installed

```bash
cd ./myproj
make
```

Now, your have a container named myproj-devenv running.

```bash
docker ps -a
```

## Use VSCode To Develop Your Project
1. Start VSCode, install Remote extention.
2. Attach to your container : myproj-devenv in VSCode
3. Open terminal. Your project folder attached to container already. Just run
    ```bash
    .vscode/install-vscode-extensions.sh
    ```
4. Reload widdow. Then python extension and other cool extensions available.


# Source code

## Prerequisition
* docker: ">= 17.06"
* docker-compose: ">= 1.26"

## Install From Code
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