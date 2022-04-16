echo "starting apache server on http://localhost:9090"
docker run --name apache --rm -v $(pwd):/app -p 9090:8080 bitnami/apache:latest

