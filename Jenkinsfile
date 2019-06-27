void setBuildStatus(String message, String state) {
	  step([
	      $class: "GitHubCommitStatusSetter",
	      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/NYU-CI/adrf-py"],
	      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
	      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
	      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
	  ]);
	}

pipeline {
    agent any

    environment {
	IMAGE_NAME = '441870321480.dkr.ecr.us-east-1.amazonaws.com/adrf-py'
        IMAGE_TAG = sh (script: "date +'secure_%Y-%m-%d_%H-%M-%S'", returnStdout: true)
        GIT_COMMIT_HASH = sh (script: "git rev-parse --short `git log -n 1 --pretty=format:'%H'`", returnStdout: true)
        GIT_COMMITER = sh (script: "git show -s --pretty=%an", returnStdout: true)
    }

    stages {
	stage('Prepare') {
            steps {
                echo 'Preparing..'
                sh 'git submodule update --init --recursive'
            }
        }
// The next stage is for all projects
	stage('Sonarqube') {
            environment {
                scannerHome = tool 'SonarQubeScanner'
            }
            steps {
                withSonarQubeEnv('ADRF Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
	stage('Build') {
            steps {
                echo 'Building..'
 //               sh 'docker build . -t ${IMAGE_NAME}:ci-${GIT_COMMIT_HASH}'
 //                  sh 'virtualenv env -p python3'
            }
        }
// This stage is for Docker projects only
//	stage('Vulnerability Scan') {
//	    steps {
//		sh '$(aws ecr get-login --no-include-email)'
//		sh 'docker push ${IMAGE_NAME}:ci-${GIT_COMMIT_HASH}'
//		writeFile file: "anchore_images", text: "${IMAGE_NAME}:ci-${GIT_COMMIT_HASH}"
//		anchore name: "anchore_images"
//	    }
//	}
	stage('Release') {
            steps {
                echo 'Releasing..'
//                sh '$(aws ecr get-login --no-include-email)'
//                sh 'docker tag ${IMAGE_NAME}:ci-${GIT_COMMIT_HASH} ${IMAGE_NAME}:${IMAGE_TAG}'
//                sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
//                sh 'docker tag ${IMAGE_NAME}:ci-${GIT_COMMIT_HASH} ${IMAGE_NAME}:${GIT_COMMIT_HASH}'
//                sh 'docker push ${IMAGE_NAME}:${GIT_COMMIT_HASH}'
            }
        }
	stage('Clean') {
            steps {
                echo 'Cleaning..'
//                sh 'docker rmi ${IMAGE_NAME}:ci-${GIT_COMMIT_HASH}'
//                sh 'docker rmi ${IMAGE_NAME}:${IMAGE_TAG}'
//                sh 'docker rmi ${IMAGE_NAME}:${GIT_COMMIT_HASH}'
            }
        }
    }
    post {
	    success {
	      slackSend (color: '#00FF00', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' by ${env.GIT_COMMITER} (${env.BUILD_URL})");
	      setBuildStatus("Build succeeded", "SUCCESS");
	    }
	    failure {
	      slackSend (color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' by ${env.GIT_COMMITER} (${env.BUILD_URL})");
	      setBuildStatus("Build failed", "FAILURE");
	    }
    }

}
