pipeline {
    agent any
    environment {
        PATH = "/var/lib/jenkins/.local/bin:$env.PATH"
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
                    sh 'pip3 install -r requirements.txt'
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
                sh "sshpass -p 'vag123' ssh -o StrictHostKeyChecking=no vagrant@192.168.56.11 'cd /home/vagrant/projet-devops && git pull && kubectl apply -f k8s/ --validate=false'"
            }
        }
    }
}