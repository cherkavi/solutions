#!/bin/bash
source vars.sh
docker exec ${DOCKER_MYSQL_DB} /bin/sh -c 'mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" < /scripts/script-dml.sql'
docker exec ${DOCKER_MYSQL_DB} /bin/sh -c 'mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" < /scripts/script-dml_config.sql'
docker exec ${DOCKER_MYSQL_DB} /bin/sh -c 'mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" < /scripts/script-dml_location.sql'
