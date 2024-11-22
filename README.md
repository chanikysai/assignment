# Kubernetes Deployment and Ingress Setup on Docker Desktop

This document outlines the steps to deploy two sample applications on a Kubernetes cluster running in Docker Desktop and set up Ingress to manage routing for the applications.

## Features
- **Rate Limiting**: Limits requests to `5 requests/min` based on the combination of client IP and `X-Client-Id` header.
- **Custom Response Code**: Returns `429 Too Many Requests` for rate-limited responses.
- **Default Logging + Custom Header**: Logs the `X-Client-Id` header along with default parameters.
- **Fallback Route**: Returns a `404` response for routes not explicitly defined.


## Prerequisites
- Docker Desktop installed with Kubernetes enabled.
- kubectl CLI installed and configured.
- Helm CLI installed for managing Kubernetes charts.
- Kubernetes cluster with Nginx Ingress Controller installed.
- Deployed backend services (`app1-service` and `app2-service`).


---

## Steps
### 1. Verify Kubernetes Cluster on Docker Desktop

    Ensure Kubernetes is enabled on Docker Desktop and verify the node status:

    ```
    $ kubectl get nodes
        NAME             STATUS   ROLES           AGE   VERSION
        docker-desktop   Ready    control-plane   12m   v1.25.0
    ```

### 2. Apply the both deployment 

    Apply the configuration:
    ```
    $ kubectl apply -f app1-deployment.yml
        deployment.apps/app1 created
        service/app1-service created
    ```

    ```
        kubectl apply -f app2-deployment.yml
        deployment.apps/app2 created
        service/app2-service created
    ```


### 3.
    Install the NGINX Ingress Controller using Helm:
    ```
        $ helm install nginx-ingress ingress-nginx/ingress-nginx
        $ kubectl get pods
        NAME                                                     READY   STATUS    RESTARTS   AGE
        app1-f6fdf9f44-9lnwh                                     1/1     Running   0          40m
        app2-58b9b958f7-wxbzt                                    1/1     Running   0          36m
        nginx-ingress-ingress-nginx-controller-c86f49c5b-m74h7   1/1     Running   0          33m
    ```


### 4.
    Configure Ingress (nginx-ingress.yaml)

    ```
         kubectl apply -f nginx-ingress.yaml
    ```

### 5. Verify Application Access
    Test access to the deployed applications using curl:

                ```
    APP1

        curl -H "X-Client-Id: test-client" http://localhost/v1
        % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                        Dload  Upload   Total   Spent    Left  Speed
        100    60  100    60    0     0   7495      0 --:--:-- --:--:-- --:--:--  8571Hello, world!
        Version: 1.0.0
        Hostname: app1-f6fdf9f44-9lnwh



    APP2

        curl -H "X-Client-Id: test-client" http://localhost/v2
        % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                        Dload  Upload   Total   Spent    Left  Speed
        100    61  100    61    0     0  11605      0 --:--:-- --:--:-- --:--:-- 15250Hello, world!
        Version: 2.0.0
        Hostname: app2-58b9b958f7-wxbzt

                ```

### 6. Verify Application Access
        For undefined routes, verify that the fallback route returns a 404 response:

        ```
        $ curl -H "X-Client-Id: test-client" http://localhost/v3
        % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                        Dload  Upload   Total   Spent    Left  Speed
        100   146  100   146    0     0  26932      0 --:--:-- --:--:-- --:--:-- 36500<html>
        <head><title>404 Not Found</title></head>
        <body>
        <center><h1>404 Not Found</h1></center>
        <hr><center>nginx</center>
        </body>
        </html>  
        
        ```

### 7 . Verify Application Access
Test rate limiting by repeatedly accessing the endpoint:


### 8 . Logging and Header Configuration

    The NGINX Ingress Controller is configured to log the X-Client-Id header for each request. Confirm this in the logs:


        ```
        192.168.65.3 - - [22/Nov/2024:11:25:14 +0000] "GET /v2 HTTP/1.1" 200 61 "-" "curl/7.83.1" 101 0.001 [default-app2-service-8080] [] 10.1.0.205:8080 61 0.001 200 6a41475ddb336c3d204ac747be28a11a
        192.168.65.3 - - [22/Nov/2024:11:51:15 +0000] "GET /v2 HTTP/1.1" 200 61 "-" "curl/7.83.1" 101 0.002 [default-app2-service-8080] [] 10.1.0.205:8080 61 0.002 200 4d13b51c9929214100b614951f864576
        192.168.65.3 - - [22/Nov/2024:11:51:36 +0000] "GET /v1 HTTP/1.1" 200 60 "-" "curl/7.83.1" 101 0.003 [default-app1-service-8080] [] 10.1.0.204:8080 60 0.004 200 317e78865f6a9a6d098b2cf5da9273b0

        ```


### File List
        app1-deployment.yml: Deployment and Service definition for App1.
        app2-deployment.yml: Deployment and Service definition for App2.
        nginx-ingress.yaml: Ingress configuration for routing and rate limiting.
        README.md: Documentation for the setup.


### Notes
    The example assumes the nginx-ingress is exposed on http://localhost. Update the address as per your setup.
    Adjust annotations in the nginx-ingress.yaml file to suit specific requirements (e.g., rate limits, headers).
    Ensure that all required backend services (app1-service and app2-service) are healthy and accessible before configuring the ingress.

