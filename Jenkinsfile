pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        sh 'pytest app/tests/gcd/'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Tests failed. Stopping pipeline."
                    }
                }
            }
        }

        stage('Merge to Main') {
            when {
                branch 'feature-branch'
            }
            steps {
                script {
                    sh '''
                    git config --global user.email "your-email@example.com"
                    git config --global user.name "Jenkins"
                    git checkout main
                    git pull origin main
                    git merge --no-ff feature-branch -m "Auto-merging feature-branch"
                    git push origin main
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline executed successfully! 🎉"
        }
        failure {
            echo "Pipeline failed! ❌ Check the logs."
        }
    }
}
