#!/bin/bash
source vars.sh
docker-compose --project-name ${PROJECT_NAME} -f mysql-with-admin.yaml up

