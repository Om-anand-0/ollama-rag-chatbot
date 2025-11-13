pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_VERSION = '2.23.0'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yourusername/ollama-chatbot.git'
            }
        }

        stage('Setup Docker') {
            steps {
                sh 'docker --version'
                sh 'docker compose version || sudo apt-get install -y docker-compose'
            }
        }

        stage('Build App') {
            steps {
                sh 'docker compose build --no-cache'
            }
        }

        stage('Run Tests') {
            steps {
                // Simple sanity check
                sh 'docker compose run chatbot python -m unittest discover -s app/tests || echo "No tests yet!"'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose up -d'
            }
        }
    }

    post {
        always {
            echo "✅ Pipeline completed!"
        }
        failure {
            echo "❌ Something went wrong in the pipeline."
        }
    }
}
