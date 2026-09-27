pipeline {
    agent any

    environment {
        IMAGE_NAME = 'student-app'
        PORT = '5000'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies & Run Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest test_app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    # Stop and remove existing container if running
                    docker stop student-app-container || true
                    docker rm student-app-container || true
                    
                    # Run new container
                    docker run -d --name student-app-container -p 5000:5000 ${IMAGE_NAME}:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}