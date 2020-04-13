Simple Web application based on UI+Lambda+DynamoDB
![architecture](https://i.postimg.cc/fRtpK5yG/aws-webapp-architecture-example.png)

# Domain model
![domain model](https://i.postimg.cc/L5Q77MBV/RB-2020-04-13-00-36-08.jpg)
![convert to OpenAPI](https://i.postimg.cc/xjNXQkjG/aws-webapp-solution-model-generation.png)

## create OpenAPI specification
* [web designer](https://stoplight.io/studio/)
* [designer](https://www.apicur.io/)
    ```sh
    git clone https://github.com/Apicurio/apicurio-studio.git
    cd apicurio-studio/distro/docker-compose
    cat Readme.md
    ```

## generate server/client mock
```bash
docker rm openapi-mock
docker run -it \
    --name=openapi-mock \
    -p 4010:4010 \
    -v $(pwd)/back2ussr.v1.yaml:/app/config.yaml \
    stoplight/prism \
    mock --dynamic --host 0.0.0.0 /app/config.yaml
```


## generate server/client code
```bash
docker pull swaggerapi/swagger-editor
docker run -d -p 8090:8080 swaggerapi/swagger-editor
```    


# AWS

