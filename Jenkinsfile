pipeline {
  agent any

  environment {
    DDASH_IMAGE = "${env.DOCKER_REGISTRY}/${params.NAMESPACE}/ddash:${env.BUILD_NUMBER}"
    NAMESPACE = "${params.NAMESPACE}"
    INGRESS = "${params.INGRESS}"
  }

  stages {

    stage('Build Image') {
      steps {
        script {
          docker.build(DDASH_IMAGE)
        }
      }
    }
    stage('Push Image') {
      steps {
        script {
          withCredentials([[$class: 'FileBinding', credentialsId: "gcr-jenkins-secret", variable: 'GCR_KEY_FILE']]) {
            sh "docker login -u _json_key --password-stdin https://gcr.io < $GCR_KEY_FILE \
            && docker push $DDASH_IMAGE"
          } 
        }
      }
    }
    stage('Deploy') {
      steps {
        script {
          kubernetesDeploy(
            kubeconfigId: 'duara-kubeconfig',
            configs: 'deployment/*.yaml',
            enableConfigSubstitution: true,
          )
        }
      }
    }
  }
}
