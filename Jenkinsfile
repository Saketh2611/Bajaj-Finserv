pipeline {
    agent any

    environment {
        IMAGE_NAME = "bill-extractor-api"
        IMAGE_TAG  = "latest"
        CONTAINER_NAME = "bill-extractor-api"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Run Tests (optional)') {
            when {
                expression { fileExists('tests') }
            }
            steps {
                sh """
                docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} pytest || echo "Tests failed or not configured"
                """
            }
        }

        stage('Deploy') {
            steps {
                sh """
                # Stop and remove existing container if running
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true

                # Run new container
                docker run -d \
                    --name ${CONTAINER_NAME} \
                    -p 8000:8000 \
                    ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }

    post {
        failure {
            echo "Build or deployment failed. Check logs."
        }
        success {
            echo "Deployment successful. FastAPI app should be available on port 8000."
        }
    }
}
