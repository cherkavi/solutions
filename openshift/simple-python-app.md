1. create route
```sh
ROUTE_NAME=sticky-sessions
OCP_PROJECT=simple-application-staging-03

# oc create inline  oc document here
cat <<EOF | oc apply -f -
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: $ROUTE_NAME
spec:
  host: $ROUTE_NAME-stg-3.vantage.zu
  to:
    kind: Service
    name: $ROUTE_NAME
  port:
    targetPort: 9090
  tls:
    insecureEdgeTerminationPolicy: None
    termination: edge
EOF

oc get route $ROUTE_NAME -o yaml
# oc delete route $ROUTE_NAME
```
2. create service
```sh
SERVICE_NAME=sticky-sessions
OCP_PROJECT=simple-application-staging-03

cat <<EOF | oc apply -f -
apiVersion: v1
kind: Service
metadata:
  name: $SERVICE_NAME
  namespace: $OCP_PROJECT
spec:
  ports:
  - name: 9090-tcp
    port: 9090
    protocol: TCP
    targetPort: 9090
  selector:
    app: $SERVICE_NAME
  sessionAffinity: None  
  type: ClusterIP
EOF

oc get service $SERVICE_NAME -o yaml
# oc delete service $SERVICE_NAME
```
3. start pod ( create deployment )
```sh
DEPLOYMENT_NAME=sticky-sessions
OCP_PROJECT=simple-application-staging-03
CONTAINER_URI=default-route-openshift-image-registry.vantage.zu/python3:20230229

cat <<EOF | oc apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
    name: $DEPLOYMENT_NAME
spec:
    # replicas: 3
    selector:
        matchLabels:
            app: $DEPLOYMENT_NAME
    template:
        metadata:
            labels:
                app: $DEPLOYMENT_NAME
        spec:
            containers:
            - name: html-container
              image: $CONTAINER_URI
              command: ["sleep", "3600"]
              ports:
                - containerPort: 9090
EOF

oc get deployment $DEPLOYMENT_NAME -o yaml
# oc delete deployment $DEPLOYMENT_NAME
```
4. inside pod start python application on specific port
    1. create python application
```py
cat <<EOF > app.py
from http.server import BaseHTTPRequestHandler, HTTPServer

class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html"); self.end_headers() # curl: (1) Received HTTP/0.9 when not allowed
        
        self.wfile.write(f"remote_addr:{self.client_address[0]} <br />\n".encode("utf-8"))
        for each_header in self.headers:
            self.wfile.write(f"{each_header}   {self.headers[each_header]} <br />\n".encode("utf-8"))

if __name__ == '__main__':
    server_address = ('', 9090)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print('Server is running on http://localhost:9090')
    httpd.serve_forever()
EOF
```
    2. copy source code to the container
```sh
DEPLOYMENT_NAME=sticky-sessions
OCP_PROJECT=simple-application-staging-03

pod_name=`oc get pods | grep Running | grep $DEPLOYMENT_NAME | awk '{print $1}'`
oc cp app.py $pod_name:/app.py
oc rsh $pod_name
bash
cat app.py
python3 app.py
```

    3. execute curl request to route
```sh
curl https://sticky-sessions-stg-3.vantage.zu
```
