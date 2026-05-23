@Library('Shared') _
pipeline {
    agent any
    
    environment{
        SONAR_HOME = tool "Sonar"
    }
    parameters {
        string(name: 'SIMPLCASH_DOCKER_TAG', defaultValue: '', description: 'Setting docker image for latest push')
        string(name: 'DATABASE_DOCKER_TAG', defaultValue: '', description: 'Setting docker image for latest push')
    }
    stages{
        stage("Validate Parameters") {
            steps {
                script {
                    if (params.SIMPLCASH_DOCKER_TAG == '' || params.DATABASE_DOCKER_TAG == '') {
                        error("DATABASE_DOCKER_TAG and SIMPLCASH_DOCKER_TAG must be provided.")
                    }
                }
            }
        }
        stage("Workspace cleanup"){
            steps{
                script{
                    cleanWs()
                }
            }
        }
        stage('Git: Code Checkout') {
            steps {
                script{
                    code_checkout("https://github.com/arpitj105/Docker-Projects.git","simplcash")
                }
            }
        }
        stage("Trivy: Filesystem scan"){
            steps{
                script{
                    trivy_scan()
                }
            }
        }
        stage("OWASP: Dependency check"){
            steps{
                script{
                    owasp_dependency()
                }
            }
        }
        stage("SonarQube: Code Analysis"){
            steps{
                script{
                    sonarqube_analysis("Sonar","SimplCash","SimplCash")
                }
            }
        }
        stage("SonarQube: Code Quality Gates"){
            steps{
                script{
                    sonarqube_code_quality()
                }
            }
        }
        stage("Docker: Build Images"){
            steps{
                script{
                    dir('Database'){
                        docker_build("simplcash-db","${params.DATABASE_DOCKER_TAG}","arpitjd105")
                    }
                    docker_build("simplcash","${params.SIMPLCASH_DOCKER_TAG}","arpitjd105")
                }
            }
        }
        stage("Docker: Push to DockerHub"){
            steps{
                script{
                    docker_push("simplcash","${params.SIMPLCASH_DOCKER_TAG}","arpitjd105")
                    docker_push("simplcash-db","${params.DATABASE_DOCKER_TAG}","arpitjd105")
                }
            }
        }
    }
    post{
        success{
            archiveArtifacts artifacts: '*.xml', followSymlinks: false
            build job: "Simplcash-CD", parameters: [
                string(name: 'SIMPLCASH_DOCKER_TAG', value: "${params.SIMPLCASH_DOCKER_TAG}"),
                string(name: 'DATABASE_DOCKER_TAG', value: "${params.DATABASE_DOCKER_TAG}")
            ]
        }
    }
}
