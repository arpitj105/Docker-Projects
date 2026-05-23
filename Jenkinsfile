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
                            docker_build("SimplCash","${params.DATABASE_DOCKER_TAG}","arpitjd105")
                        }
            
                            docker_build("SimplCash","${params.SIMPLCASH_DOCKER_TAG}","arpitjd105")
                        
                }
            }
        }

        stage("Docker: Push to DockerHub"){
            steps{
                script{
                    docker_push("SimplCash","${params.SIMPLCASH_DOCKER_TAG}","arpitjd105") 
                    docker_push("SimplCash","${params.DATABASE_DOCKER_TAG}","arpitjd105")
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

































        
                     
                    
                  
                 
             
          
              
           
                 
                                
                       
                        
                       
                          
                  
                                 
                         
        
        // stage("Code"){
        //     steps{
        //     git url: "https://github.com/arpitj105/Docker-Projects.git", branch: "master"    
            
                
        //     }
        // }
        // stage("Build and test"){
        //     steps{
        //         dir("simplcash"){
        //             sh "docker build -t simplcash-app-jenkins:latest ."    
                    
                    
        //         }
            
        //     }
        // }
        // stage("Pushed to DockerHub"){
        //     steps{
        //         withCredentials(
        //            [usernamePassword(
        //                credentialsId: "dockerCreds",
        //                passwordVariable: "dockerHubPass",
        //                usernameVariable: "dockerHubuser")
        //             ]){
        //                 dir("simplcash"){
        //                    sh "docker image tag simplcash-app-jenkins:latest ${env.dockerHubuser}/simplcash-app-jenkins:latest"
        //                    sh "docker login -u ${env.dockerHubuser} -p ${env.dockerHubPass}"
        //                    sh "docker push ${env.dockerHubuser}/simplcash-app-jenkins:latest"
        //                 }   
        //             }
        //     }
        // }
        
        // stage("Deploy"){
        //     steps{
        //     dir("simplcash"){
        //     sh "docker network create simplcash-network || true" 
        //     sh "sleep 30"
        //     sh "docker run -d -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=simplcashdb --network simplcash-network -v simplcash-mysql:/var/lib/mysql --name simplcashmysql mysql:5.7"
        //     sh "sleep 30"
        //     sh "docker run -d -p 5002:5000 -v simplcash-mysql:/var/lib/mysql --network simplcash-network -e MYSQL_HOST=simplcashmysql -e MYSQL_USER=root -e MYSQL_PASSWORD=root -e MYSQL_DB=simplcashdb -e SECRET_KEY=test --name simplcashflask simplcash-app-jenkins:latest"
            
        //     }
        //     }
        // }
//     }
// }
