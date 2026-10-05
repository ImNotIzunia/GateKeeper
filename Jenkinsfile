pipeline {
    agent any

    stages {
        stage('Install Python') {
            steps {
                sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3 python3-pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Export Data') {
            steps {
                sh '''
                    python3 export.py
                '''
            }
        }

        stage('Upload to storage server') {
            steps {
                sh '''
                    chmod +x copy.sh
                    ./copy.sh
                '''
                cleanWs()
            }
        }
    }
}