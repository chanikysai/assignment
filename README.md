# Setting up Kubernetes with Minikube and Jenkins

This guide, this prepared by Venkatsai, will walk you through setting up Kubernetes using Minikube on my local machine, deploying Jenkins using Helm, and configuring a local Docker registry using Docker Compose.

## Prerequisites

1. **Minikube**: Install Minikube to run a local Kubernetes cluster.
2. **Docker**: Ensure Docker is installed to build and run Docker images.
3. **Helm**: Install Helm to manage Kubernetes applications.
4. **kubectl**: Install kubectl to interact with Kubernetes clusters.

## Step 1: Starting Minikube

```bash
venkatsai@venkats-MacBook-Air ~ % minikube start
  minikube v1.31.2 on Darwin 14.3 (arm64)
✨  Using the docker driver based on existing profile
  Starting control plane node minikube in cluster minikube
  Pulling base image ...
  Restarting existing docker container for "minikube" ...
  Preparing Kubernetes v1.27.4 on Docker 24.0.4 ...
  Configuring bridge CNI (Container Networking Interface) ...
  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
  Enabled addons: storage-provisioner, default-storageclass
  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```


##  Step 2: Verifying Minikube Node
```bash

venkatsai@venkats-MacBook-Air ~ % kubectl get nodes -o wide
NAME       STATUS   ROLES           AGE    VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION    CONTAINER-RUNTIME
minikube   Ready    control-plane   200d   v1.27.4   192.168.49.2   <none>        Ubuntu 22.04.2 LTS   6.6.31-linuxkit   docker://24.0.4

```


This output confirms that Minikube is running and Kubernetes cluster components are verified.



## Step 3: Installing Helm and Jenkins
```bash
Adding Helm Repository for Jenkins

venkatsai@venkats-MacBook-Air ~ % helm repo add jenkins https://charts.jenkins.io
"jenkins" already exists with the same configuration, skipping

## Updating Helm Repositories

venkatsai@venkats-MacBook-Air ~ % helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "jenkins" chart repository
Update Complete. ⎈Happy Helming!⎈

## Installing Jenkins via Helm

venkatsai@venkats-MacBook-Air ~ % helm install jenkins -n jenkins jenkins/jenkins
NAME: jenkins
LAST DEPLOYED: Tue Jun 25 09:36:07 2024
NAMESPACE: jenkins
STATUS: deployed
REVISION: 1


## Verifying Jenkins Installation

venkatsai@venkats-MacBook-Air ~ % kubectl get pods -n jenkins
NAME                 READY   STATUS   RESTARTS   AGE
jenkins-0            2/2     Running   7          11h



## Accessing Jenkins

venkatsai@venkats-MacBook-Air ~ % kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/additional/chart-admin-password && echo
ojZItPrqD5SzoLEuGZyP1i


## Retrieve the Jenkins admin password using the command above. Then, set up port forwarding to access the Jenkins UI:


venkatsai@venkats-MacBook-Air ~ % kubectl --namespace jenkins port-forward svc/jenkins 8080:8080
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080


## Access Jenkins by navigating to http://127.0.0.1:8080 in your web browser.


![Screenshot](kubectl.png)

```

## Step 4: Setting up Docker Registry using Docker Compose

```bash

Docker Compose Configuration
Create a docker-compose.yml file with the following content:
version: "3"
services:
  docker-registry:
    image: registry:2
    container_name: registry
    ports:
      - 5000:5000
    restart: always
    volumes:
      - ./docker-registry:/var/lib/registry

  docker-registry-ui:
    image: konradkleine/docker-registry-frontend:v2
    container_name: registry_ui
    ports:
      - 8080:80
    restart: always
    environment:
      ENV_DOCKER_REGISTRY_HOST: docker-registry
      ENV_DOCKER_REGISTRY_PORT: 5000

## Starting Docker Registry


venkatsai@venkats-MacBook-Air ~ % mkdir compose
venkatsai@venkats-MacBook-Air ~ % cd compose
venkatsai@venkats-MacBook-Air compose % vi docker-compose.yml
venkatsai@venkats-MacBook-Air compose % docker-compose up -d

```

## Step 5: Jenkins Pipeline for Docker Image Build and Push
```bash

Jenkinsfile Configuration
Add the following Jenkins Pipeline script (Jenkinsfile):



pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent'
            yaml """
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: jnlp
                image: jenkins/inbound-agent
                args: ['\$(JENKINS_SECRET)', '\$(JENKINS_NAME)']
              - name: docker
                image: docker:20.10
                command:
                - cat
                tty: true
                volumeMounts:
                - name: docker-sock
                  mountPath: /var/run/docker.sock
            volumes:
            - name: docker-sock
              hostPath:
                path: /var/run/docker.sock
            """
        }
    }
    stages {
        stage('Dummy Task') {
            steps {
                container('jnlp') {
                    echo "Hello from Jenkins running in a Kubernetes pod!"
                }
            }
        }
        stage('Create Dockerfile') {
            steps {
                container('jnlp') {
                    script {
                        writeFile file: 'Dockerfile', text: '''
                        # Use the official Python image from the Docker Hub
                        FROM python:3.9-slim
                        # Set the working directory
                        WORKDIR /app
                        # Copy the current directory contents into the container at /app
                        COPY . /app
                        # Define environment variable
                        ENV NAME=World
                        # Run a simple echo command
                        CMD ["sh", "-c", "echo Hello, $NAME"]
                        '''
                    }
                }
            }
            stage('Build Docker Image') {
                steps {
                    container('docker') {
                        script {
                            def imageTag = "localhost:5000/my-image:${env.BUILD_NUMBER}"
                            sh "docker build -t ${imageTag} ."
                        }
                    }
                }
            }
            stage('Push Docker Image') {
                steps {
                    container('docker') {
                        script {
                            def imageTag = "localhost:5000/my-image:${env.BUILD_NUMBER}"
                            sh "docker push ${imageTag}"
                        }
                    }
                }
            }
        }
        post {
            always {
                container('jnlp') {
                    cleanWs()
                }
            }
        }
    }
}

![Screenshot](jenkins.png)

```

## Step 6: Whenever the new build has been triggered it is launching new pod in kubernetes
```bash
![Screenshot](agentpod.png)

![Screenshot](docker_registry.png)


```


