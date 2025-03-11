pipeline {
    agent any  // Run on any available Jenkins agent
    
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'git@github.com:sakethsram/saketh-api.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'  // Install dependencies
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest app/tests/gcd'  // Run tests
            }
        }
    }
}
