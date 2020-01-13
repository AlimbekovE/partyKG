pipeline {
    agent any

    stages {
        stage('BUILD') {
            steps {
                echo 'Building docker environment...'
                sh "docker network create --driver bridge nw_${env.BUILD_TAG}"
                sh "docker run --network=nw_${env.BUILD_TAG} -itd --name=postgres_${env.BUILD_TAG} postgres"
            }
        }
        stage('Test') {
            steps {
                echo "Testing..."
                sh "docker run --network=nw_${env.BUILD_TAG} --name=kp_${env.BUILD_TAG} -v ${env.WORKSPACE}/web:/usr/src/app -w /usr/src/app -e 'POSTGRES_HOST=postgres_${env.BUILD_TAG}' -e 'PGBOUNCER_HOST=postgres_${env.BUILD_TAG}'  -e 'PGBOUNCER_PORT=5432' -e 'PYTHONDONTWRITEBYTECODE=1' python:3.8 bash -c 'pip install -r requirements.txt && python manage.py test'"
            }
        }
        stage('Deploy Staging') {
            when {
                expression { env.BRANCH_NAME == 'develop' }
            }
            steps {
                echo "Deploying image..."
                sh "scp docker-compose-devel.yml root@kp.mirsoft.io:/root/staging.kp.kg/docker-compose-devel.yml"
                sh "docker build -f web/Dockerfile --target production -t ms-kp ./web"
                sh "docker build -f nginx/Dockerfile -t ms-kp-nginx ./nginx"
                sh "docker tag ms-kp mirsoftdevel/kp:web-develop"
                sh "docker tag ms-kp-nginx mirsoftdevel/kp:nginx-develop"
                withDockerRegistry([credentialsId: 'fc62ace4-e6c7-4451-9173-fd536f61890b', url: ' https://index.docker.io/v1/']) {
                    sh "docker push mirsoftdevel/kp:web-develop"
                    sh "docker push mirsoftdevel/kp:nginx-develop"

                }
            }
        }
        stage('Deploy Production') {
            when {
                expression { env.BRANCH_NAME == 'master' }
            }
            steps {
                echo "Deploying image..."
                sh "scp docker-compose-prod.yml root@kg7.kg:/root/kp/docker-compose-prod.yml"
                sh "docker build -f web/Dockerfile --target production -t ms-kp ./web"
                sh "docker build -f nginx/Dockerfile -t ms-kp-nginx ./nginx"
                sh "docker tag ms-kp mirsoftdevel/kp:web"
                sh "docker tag ms-kp-nginx mirsoftdevel/kp:nginx"
                withDockerRegistry([credentialsId: '0a3b80bb-a5d8-45f1-aec0-cad050f8770d', url: ' https://index.docker.io/v1/']) {
                    sh "docker push mirsoftdevel/kp:web"
                    sh "docker push mirsoftdevel/kp:nginx"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning...'
            script {
                try {
                    sh "docker stop kp_${env.BUILD_TAG} postgres_${env.BUILD_TAG} 2>/dev/null"
                    sh "docker rm kp_${env.BUILD_TAG} postgres_${env.BUILD_TAG} 2>/dev/null"
                    sh "docker network rm nw_${env.BUILD_TAG} 2>/dev/null"
                    deleteDir()

                } catch(err) {
                    echo "deleteDir error: ${err}"
                }
            }

        }
    }
}
