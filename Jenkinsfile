pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                script {
                    def branch = env.BRANCH_NAME ?: 'main'
                    checkout([$class: 'GitSCM', 
                        branches: [[name: "*/${branch}"]],
                        userRemoteConfigs: [[url: 'https://github.com/sakethsram/saketh-api.git']]
                    ])
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python -m pytest app/tests/gcd/'
            }
        }
    }
}
