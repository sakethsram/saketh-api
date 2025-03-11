pipeline {
    agent any

    stages {
        stage('Checkout Feature Branch') {
            steps {
                script {
                    // Clone the feature branch
                    checkout([$class: 'GitSCM', 
                        branches: [[name: 'origin/feature-branch']],
                        userRemoteConfigs: [[url: 'git@github.com:sakethsram/saketh-api.git']]
                    ])
                }
            }
        }

        stage('Run Tests on Feature Branch') {
            steps {
                sh 'pytest app/tests/gcd'
            }
        }

        stage('Check Merge Conflict') {
            steps {
                script {
                    def mergeOutput = sh(script: "git checkout main && git pull origin main && git merge --no-commit --no-ff feature-branch", returnStatus: true)
                    if (mergeOutput != 0) {
                        error("Merge conflict detected! Resolve conflicts before merging.")
                    }
                }
            }
        }

        stage('Merge to Main') {
            steps {
                script {
                    sh "git commit -m 'Merged feature-branch into main' && git push origin main"
                }
            }
        }

        stage('Run Tests on Main') {
            steps {
                sh 'pytest app/tests/gcd'
            }
        }
    }
}
