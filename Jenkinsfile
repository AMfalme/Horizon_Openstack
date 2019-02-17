/* import shared library */
@Library('jenkins-shared-library')_

pipeline {
  agent any

  environment {
    DOCKER_REGISTRY = "gcr.io"
    PROJECT_ID = "robotic-fuze-194312"
    NAME = "${env.JOB_NAME}"
    CONTAINER_NAME = "${NAME.replaceAll('/', '_')}"
    GIT_SHA = sh (script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
    GCR_IMAGE = "$DOCKER_REGISTRY/$PROJECT_ID/$NAME"
    GCR_IMAGE_SHA = "$GCR_IMAGE:$GIT_SHA"
    GCR_IMAGE_LATEST = "$GCR_IMAGE:latest"

    CONTAINER_PORT="80"
    PROD_HOST_PORT="8070"
    STAGING_HOST_PORT="9070"
    DOCKER_NET="docker-net"
    // Machines
    PROD_MACHINE = "ddash.staging"
    PROD_ENV = "~/.env/ddash.staging.env"
    STAGING_MACHINE = "diam.staging"
    STAGING_ENV = "~/.env/diam.staging.env"
    DNS_SERVER = "10.0.0.2"
  }

  stages {
    stage('Build Image') {
      steps {
        script {
          docker.build(GCR_IMAGE, ".")
        }
      }
    }
    stage('Publish Image') {
      when {
        anyOf {
          branch 'staging';
          branch 'release'
        }
      }
      steps {
        script {
          withCredentials([[$class: 'FileBinding', credentialsId: "gcr-jenkins-ci-secret", variable: 'GCR_KEY_FILE']]) {
            sh "docker login -u _json_key --password-stdin https://gcr.io < $GCR_KEY_FILE \
              && docker tag $GCR_IMAGE $GCR_IMAGE_SHA \
              && docker tag $GCR_IMAGE $GCR_IMAGE_LATEST \
              && docker push $GCR_IMAGE_SHA \
              && docker push $GCR_IMAGE_LATEST"
          }
        }
      }
    }
    stage('Deploy Staging') {
      when {
        branch 'staging'
      }
      environment {
        ENV_FILE = "$STAGING_ENV"
        STAGE = "staging"
      }
      steps {
        script {
          def remote = [:]
          remote.name = "$STAGING_MACHINE"
          remote.host = "$STAGING_MACHINE"
          remote.allowAnyHosts = true
          withCredentials([sshUserPrivateKey(credentialsId: 'jenkins-private-key', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
            remote.user = userName
              remote.identityFile = identity
              stage('Pull and Run image') {
                sshCommand remote: remote, command: "docker pull $GCR_IMAGE_LATEST"
                sshCommand remote: remote, command: "docker stop $CONTAINER_NAME || true"
                sshCommand remote: remote, command: "docker rm $CONTAINER_NAME || true"
                sshCommand remote: remote, command: "docker run -d -p $STAGING_HOST_PORT:$CONTAINER_PORT -e STAGE=$STAGE --env-file $ENV_FILE --network $DOCKER_NET --dns=$DNS_SERVER --restart=always --name $CONTAINER_NAME $GCR_IMAGE_LATEST"
                sshCommand remote: remote, command: "docker system prune -f"
              }
          }
        }
      }
    }
    stage('Deploy Production') {
      when {
        branch 'release'
      }
      environment {
        ENV_FILE = "$PROD_ENV"
        STAGE = "prod"
      }
      steps {
        script {
          def remote = [:]
            remote.name = "$PROD_MACHINE"
            remote.host = "$PROD_MACHINE"
            remote.allowAnyHosts = true
            withCredentials([sshUserPrivateKey(credentialsId: 'jenkins-private-key', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
              remote.user = userName
                remote.identityFile = identity
                stage('Pull and Run image') {
                  sshCommand remote: remote, command: "docker pull $GCR_IMAGE_LATEST"
                    sshCommand remote: remote, command: "docker stop $CONTAINER_NAME || true"
                    sshCommand remote: remote, command: "docker rm $CONTAINER_NAME || true"
                    sshCommand remote: remote, command: "docker run -d -p $PROD_HOST_PORT:$CONTAINER_PORT -e STAGE=$STAGE --env-file $ENV_FILE --network $DOCKER_NET --dns=$DNS_SERVER --restart=always --name $CONTAINER_NAME $GCR_IMAGE_LATEST"
                    sshCommand remote: remote, command: "docker system prune -f"
                }
            }
        }
      }
    }
  }

  post {
    always {
      /* Use slackNotifier.groovy from shared library and provide current build result as parameter */
      slackNotifier(currentBuild.currentResult)
    }
  }
}
