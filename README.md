# Setting up Local Docker Registry and Jenkins Integration

This guide provides steps to set up a local Docker Registry and integrate it with Jenkins pipelines for local development environments.

## Setup Local Docker Registry

1. **Docker Registry Installation**
   - Create a `docker-compose.yml` file to set up the Docker Registry and Registry UI:

     ```yaml
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
           - ENV_DOCKER_REGISTRY_HOST=docker-registry
           - ENV_DOCKER_REGISTRY_PORT=5000
     ```

2. **Start the Docker Registry**
   - Run `docker-compose up -d` in the directory containing `docker-compose.yml` to start the registry and UI.

3. **Configure Docker for Insecure Registry**
   - Add your local registry IP address to Docker's insecure registries list:
     - Edit or create `/etc/docker/daemon.json` (Linux) or `~/.docker/daemon.json` (macOS) with:

       ```jsoAccess Jenkins

Retrieve Jenkins admin password:

sh
Copy code
kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/chart-admin-password
Port-forward to access Jenkins UI:

sh
Copy code
kubectl --namespace jenkins port-forward svc/jenkins 8080:8080
Open http://localhost:8080 and login with admin password.

Jenkins Pipeline

Create a Jenkins pipeline to build and push Docker images to your local registry:

groovy
Copy code
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
        stage('Build and Push Docker Image') {
            steps {
                container('docker') {
                    script {
                        def imageTag = "your-local-registry-ip:5000/my-image:${env.BUILD_NUMBER}"
                        sh "docker build -t ${imageTag} ."
                        sh "docker push ${imageTag}"
                    }
                }
            }
        }
    }
}
Further Customizations

Configure security, backup, and other settings as per your requirements.
Consider adding Jenkins configuration as code for reproducibility.
Cleanup

Ensure to properly secure and manage your Docker Registry and Jenkins setup, especially if exposing to external environments.
This README.md provides a basic setup guide. Adjust configurations and scripts based on your specific environment and security needs.

sql
Copy code

### Notes:
- Replace `"your-local-registry-ip"` with the actual IP address where your Docker Registry is hosted.
- Include any additional steps or configurations specific to your environment or security requirements.
- Ensure to update Docker and Kubernetes versions as necessary based on your local setup.
  
This README provides a structured approach to setting up and integrating a local Docker Registry with Jenkins, aimed at facilitating local development workflows effectively. Adjustments can be made based on specific requirements or additional features needed for your environment.





n
       {
         "registry-mirrors": [],
         "insecure-registries": [
           "your-local-registry-ip:5000"
         ]
       }
       ```

     - Restart Docker: `sudo systemctl restart docker` (Linux) or restart Docker Desktop (macOS).

4. **Verify Registry**
   - Test pulling an image from your local registry:
     ```sh
     docker pull your-local-registry-ip:5000/image-name:tag
     ```

## Jenkins Integration

1. **Install Jenkins and Helm Chart**

   ```sh
   helm repo add jenkins https://charts.jenkins.io
   helm repo update
   helm install jenkins -n jenkins jenkins/jenkins
Access Jenkins

Retrieve Jenkins admin password:

sh
Copy code
kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/chart-admin-password
Port-forward to access Jenkins UI:

sh
Copy code
kubectl --namespace jenkins port-forward svc/jenkins 8080:8080
Open http://localhost:8080 and login with admin password.

Jenkins Pipeline

Create a Jenkins pipeline to build and push Docker images to your local registry:

groovy
Copy code
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
        stage('Build and Push Docker Image') {
            steps {
                container('docker') {
                    script {
                        def imageTag = "your-local-registry-ip:5000/my-image:${env.BUILD_NUMBER}"
                        sh "docker build -t ${imageTag} ."
                        sh "docker push ${imageTag}"
                    }
                }
            }
        }
    }
}
Further Customizations

Configure security, backup, and other settings as per your requirements.
Consider adding Jenkins configuration as code for reproducibility.
Cleanup

Ensure to properly secure and manage your Docker Registry and Jenkins setup, especially if exposing to external environments.
This README.md provides a basic setup guide. Adjust configurations and scripts based on your specific environment and security needs.

sql
Copy code

### Notes:
- Replace `"your-local-registry-ip"` with the actual IP address where your Docker Registry is hosted.
- Include any additional steps or configurations specific to your environment or security requirements.
- Ensure to update Docker and Kubernetes versions as necessary based on your local setup.
  
This README provides a structured approach to setting up and integrating a local Docker Registry with Jenkins, aimed at facilitating local development workflows effectively. Adjustments can be made based on specific requirements or additional features needed for your environment.








