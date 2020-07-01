#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
pushd $script_dir
docker_cli_args=$(sed -e '/^[ \t]*\/\//d' devcontainer.json | jq '.runArgs[]' | xargs)
container_name=$(sed -e '/^[ \t]*\/\//d' devcontainer.json | jq '.name' | xargs) 
popd

# make extensions arguments
docker_cli_arg_str=
for i in $docker_cli_args;  do
    docker_cli_arg_str="$docker_cli_arg_str $i"
done

pushd $script_dir/..
tag_name=$container_name:dev
docker build . --tag=$tag_name -f Dockerfile-dev
docker container rm -f $container_name
docker run -d \
    --name $container_name \
    $docker_cli_args \
    -v $(pwd):/workspaces/${PWD##*/} \
    $tag_name \
    tail -f > /dev/null
popd 
