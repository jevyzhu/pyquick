user_id=$(id -u ${USER})
group_id=$(id -g ${USER})
docker-compose build --build-arg USER_ID=$user_id --build-arg GROUP_ID=$group_id
docker-compose up -d 
