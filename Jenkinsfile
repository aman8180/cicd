pipeline {
    agent any

    environment {
        DOCKER_CRED = 'dockerhub-creds'        // Jenkins credential ID for Docker Hub
        GIT_CRED    = 'github-creds'           // Jenkins credential ID for GitHub PAT
        IMAGE_REPO  = 'amanparyani/cicd'       // Your Docker Hub repo
        IMAGE_TAG   = "${env.BUILD_NUMBER}"    // Build number as tag
        KUBECONFIG  = '/var/lib/jenkins/.kube/config'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/aman8180/cicd.git', credentialsId: "${GIT_CRED}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_REPO}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Login & Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CRED}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker push ${IMAGE_REPO}:${IMAGE_TAG}
                        '''
                    }
                }
            }
        }

        stage('Deploy to Kubernetes via Ansible') {
            steps {
                script {
                    sh '''
                        export IMAGE_TAG=${IMAGE_TAG}
                        export KUBECONFIG=${KUBECONFIG}
                        ansible-playbook ansible/deploy.yml
                    '''
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
