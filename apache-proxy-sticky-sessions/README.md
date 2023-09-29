# Emulate Sticky session using Apache Web Server

## Start Service1
```sh
python3 service1/http-server.py
curl -X GET localhost:9091
```
## Start Service2
```sh
python3 service2/http-server.py
curl -X GET localhost:9092
```

## Start apache
## context
![context diagram](https://i.ibb.co/PcGjsz8/apache-sticky.jpg)

## create conf file for apache ( copy file from container and make necessary changes in config) 
```sh
docker run --name apache --rm -v $(pwd):/app -p 9090:8080 -it bitnami/apache:latest sh
cp /opt/bitnami/apache/conf/httpd.conf /app
```

### start apache with config file
```sh
# start docker conatiner 
docker stop apache; docker rm apache; docker run --name apache --network="host" -v $(pwd)/apache-proxy.conf:/opt/bitnami/apache/conf/httpd.conf bitnami/apache:latest

# check start of apache 
curl -L -X GET localhost:8080
```

### start apache manually
```sh
docker run --name apache --network="host" -v $(pwd)/apache-proxy.conf:/opt/bitnami/apache/conf/httpd.conf -it bitnami/apache:latest sh
cd /opt/bitnami/scripts/apache

. libapache.sh
. libos.sh
. liblog.sh
. apache-env.sh

APACHE_CONF_FILE=/opt/bitnami/apache/conf/httpd.conf
APACHE_BIN_DIR=/opt/bitnami/apache/bin
"${APACHE_BIN_DIR}/httpd" -f "$APACHE_CONF_FILE"
# "${APACHE_BIN_DIR}/httpd" -f "$APACHE_CONF_FILE" -D "FOREGROUND"
```

## check redirection
```sh
### option: redirect with root
curl -L -X GET localhost:8080

### option: redirect with service 
 curl -L -X GET localhost:8080/service

## option 3 - redirect with header
curl -L -X GET -H "my-number:10.10.1.1" localhost:8080/service
curl -L -X GET -H "my-number:10.10.1.2" localhost:8080/service
```
