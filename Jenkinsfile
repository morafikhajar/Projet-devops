pipeline {
    agent any

    environment {
        DOCKERHUB_CRED = 'dockerhub-credentials'
        IMAGE_NAME = 'morafikhajar/todo-app'
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/morafikhajar/Projet-devops.git'
            }
        }

        stage('Test') {
            steps {
                sh 'pip install -r app/requirements.txt -r app/requirements-prod.txt'
                sh 'pytest app/test_app.py'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t \ ./app'
            }
        }

        stage('Push DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "\", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo \ | docker login -u \ --password-stdin'
                    sh 'docker push \'
                }
            }
        }

        stage('Deploy K8s') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
}
