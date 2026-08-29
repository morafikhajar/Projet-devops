pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        IMAGE_NAME = "morafikhajar/projet-devops-taches"
    }

    stages {
        stage('Clone') {
            steps {
                checkout scm
            }
        }

        stage('Tests unitaires') {
            steps {
                dir('app') {
                    sh 'pip install -r requirements.txt --break-system-packages'
                    sh 'pytest -v'
                }
            }
        }

        stage('Build Docker image') {
            steps {
                dir('app') {
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f k8s/"
            }
        }
    }
}
