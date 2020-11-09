#!/bin/bash
source vars.sh
docker-compose --project-name ${PROJECT_NAME} -f mysql-with-admin.yaml down
docker rm ${DOCKER_MYSQL_DB}
docker rm ${DOCKER_MYSQL_UI}
docker volume remove ${DOCKER_MYSQL_DB_VOLUME}
