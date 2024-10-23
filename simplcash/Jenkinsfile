pipeline{
    
    agent{
        node{
            label "dev"
        }
    }
    
    stages{
        stage("Code"){
            steps{
            git url: "https://github.com/arpitj105/Docker-Projects.git", branch: "master"    
            
                
            }
        }
        stage("Build and test"){
            steps{
                dir("simplcash"){
                    sh "docker build -t simplcash-app-jenkins:latest ."    
                    
                    
                }
            
            }
        }
        stage("Pushed to DockerHub"){
            steps{
                withCredentials(
                   [usernamePassword(
                       credentialsId: "dockerCreds",
                       passwordVariable: "dockerHubPass",
                       usernameVariable: "dockerHubuser")
                    ]){
                        dir("simplcash"){
                           sh "docker image tag simplcash-app-jenkins:latest ${env.dockerHubuser}/simplcash-app-jenkins:latest"
                           sh "docker login -u ${env.dockerHubuser} -p ${env.dockerHubPass}"
                           sh "docker push ${env.dockerHubuser}/simplcash-app-jenkins:latest"
                        }   
                    }
            }
        }
        
        stage("Deploy"){
            steps{
            dir("simplcash"){
            sh "docker network create simplcash-network || true" 
            sh "sleep 30"
            sh "docker run -d -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=simplcashdb --network simplcash-network -v simplcash-mysql:/var/lib/mysql --name simplcashmysql mysql:5.7"
            sh "sleep 30"
            sh "docker run -d -p 5002:5000 -v simplcash-mysql:/var/lib/mysql --network simplcash-network -e MYSQL_HOST=simplcashmysql -e MYSQL_USER=root -e MYSQL_PASSWORD=root -e MYSQL_DB=simplcashdb -e SECRET_KEY=test --name simplcashflask simplcash-app-jenkins:latest"
            
            }
            }
        }
    }
}
