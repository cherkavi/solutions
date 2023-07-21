Simple Web application based on UI+Lambda+DynamoDB
![architecture](https://i.postimg.cc/fRtpK5yG/aws-webapp-architecture-example.png)

# Domain model
![domain model](https://i.postimg.cc/d1CYTqzx/Selection-002.png)
![convert to OpenAPI](https://i.postimg.cc/xjNXQkjG/aws-webapp-solution-model-generation.png)

## create OpenAPI specification, api specification 
* [api web designer](https://stoplight.io/studio/)
* [build api](https://insomnia.rest/)
* [openapi designer, swagger designer](https://www.apicur.io/)
  * [online api designer](https://studio.apicur.io/apis)
  * start designer locally 
    ```sh
    git clone https://github.com/Apicurio/apicurio-studio.git
    cd apicurio-studio/distro/docker-compose
    cat Readme.md
    ```

## [server mock](https://github.com/stoplightio/prism/tree/master)
### [online tool](https://stoplight.io/open-source/prism)
### [how to customize answer](https://docs.stoplight.io/docs/prism/83dbbd75532cf-http-mocking#response-examples)
> use http-header "Prefer"
### start server locally
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

