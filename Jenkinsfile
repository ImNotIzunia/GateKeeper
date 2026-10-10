pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Export Data') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python3 export.py
                '''
            }
        }
        
        stage('Upload to storage server') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'SSH-Credential',
                        keyFileVariable: 'SSH_KEY',
                        passphraseVariable: 'SSH_PASSPHRASE',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        chmod +x copy.sh
                        ./copy.sh backup/*.conf
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}