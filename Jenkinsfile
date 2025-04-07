pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        VENV_NAME = 'farsco-venv'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV_NAME}
                    . ${VENV_NAME}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    python manage.py test
                '''
            }
        }
        
        stage('Check Security') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    pip install bandit
                    bandit -r . -x ${VENV_NAME},tests
                '''
            }
        }
        
        stage('Static Analysis') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    pip install pylint
                    pylint --disable=C0111,C0103,C0303,W0613 farsco main courses accounts
                '''
            }
        }
        
        stage('Collect Static') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    python manage.py collectstatic --noinput
                '''
            }
        }
        
        stage('Deploy to Development') {
            when {
                branch 'develop'
            }
            steps {
                echo "Deploying to Development environment"
                // Add your deployment steps here
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                echo "Deploying to Production environment"
                // Add your production deployment steps here
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
