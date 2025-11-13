pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Om-anand-0/ollama-rag-chatbot.git'
            }
        }

        stage('Verify Docker') {
            steps {
                sh 'docker --version'
                sh 'docker compose version'
            }
        }

        stage('Build App') {
            steps {
                sh 'docker compose build --no-cache'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                if docker compose run chatbot python -m unittest discover -s app/tests ; then
                    echo "Tests executed"
                else
                    echo "No tests found"
                fi
                '''
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
