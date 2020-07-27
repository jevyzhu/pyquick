#!/bin/bash
export user_id=$(id -u ${USER}) 
export group_id=$(id -g ${USER}) 
docker-compose up -d --build
#docker-compose build --build-arg USER_ID=$user_id --build-arg GROUP_ID=$group_id
