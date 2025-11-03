pipeline {
    agent any

    environment {
        DOCKER_CRED = 'dockerhub-creds'                 // 🔹 Jenkins credential ID for Docker Hub
        IMAGE_REPO  = 'amanparyani/cicd'     // 🔹 Replace with your Docker Hub repo
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/aman8180/cicd.git'   // 🔹 Replace with your repo URL
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_REPO}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CRED) {
                        sh "docker push ${IMAGE_REPO}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes via Ansible') {
            steps {
                script {
                    sh "ansible-playbook -i ansible/inventory ansible/deploy.yml --extra-vars 'image_repo=${IMAGE_REPO} image_tag=${IMAGE_TAG}'"
                }
            }
        }
    }

    post {
        success {
            echo '✅ Deployment Successful!'
        }
        failure {
            echo '❌ Build/Deployment Failed.'
        }
    }
}
