#!/bin/bash
export MYSQL_DATABASE=masterdb
export MYSQL_PORT=3306
export MYSQL_PORT_EXT=3310
export PROJECT_NAME=web
export DOCKER_MYSQL_DB=mysql_db
export DOCKER_MYSQL_DB_VOLUME=web_mysql_db
export DOCKER_MYSQL_UI=mysql_admin_panel

source .env

for each_val in "MYSQL_ROOT_PASSWORD" "MYSQL_USER" "MYSQL_PASSWORD"
do
    declare "current_variable=$each_val"
    if [ -z ${!current_variable} ]; then
        echo "file '.env' should contains value $each_val"
        exit 1
    fi
done

