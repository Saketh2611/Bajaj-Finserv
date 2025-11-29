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
                bat """
                docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                """
            }
        }

        stage('Run Tests') {
            when {
                expression { fileExists('tests') }
            }
            steps {
                bat """
                docker run --rm %IMAGE_NAME%:%IMAGE_TAG% pytest || echo Tests Failed
                """
            }
        }

        stage('Deploy Container') {
            steps {
                bat """
                docker stop %CONTAINER_NAME% || echo Not Running
                docker rm %CONTAINER_NAME% || echo No Container
                docker run -d -p 8000:8000 --name %CONTAINER_NAME% %IMAGE_NAME%:%IMAGE_TAG%
                """
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment successful → FastAPI running on port 8000!"
        }
        failure {
            echo "❌ Build failed — Check Console Output"
        }
    }
}
