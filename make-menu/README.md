# start DB locally
## prepare environment 
### adjust current environment
```sh
cp env-local-example .env
# adjust three variables inside script: "MYSQL_ROOT_PASSWORD" "MYSQL_USER" "MYSQL_PASSWORD"
```

### example of .env file
```properties
MYSQL_ROOT_PASSWORD=root
MYSQL_USER=admin
MYSQL_PASSWORD=admin
```

## start MySQL with admin panel
```sh
# open new terminal window, start container with DB
make start
```

## stop MySQL with admin panel
```sh
# execute it in case of stoping for a while ( container will be removed,  but data will stay for future start in folder "mysqldata")
make stop 

# remove docker container, remove docker network, remove volumes
make remove-all
```

## fill database up with "test" data
```sh
# DDL + DML
make write
# create all tables
make write-ddl
# create all views
make write-ddl-view
# fill up all the data into tables
make write-dml
```

## connect to Database
```bash
x-www-browser http://localhost:8080
#   server: mysql_db
# username: admin
# password: admin
# database: masterdb
```
