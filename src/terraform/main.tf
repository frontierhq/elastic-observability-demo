provider "ec" {}

provider "elasticstack" {
  elasticsearch {
    endpoints = [ec_deployment.main.elasticsearch.https_endpoint]
    username  = ec_deployment.main.elasticsearch_username
    password  = ec_deployment.main.elasticsearch_password
  }
  kibana {
    endpoints = [ec_deployment.main.kibana.https_endpoint]
    username  = ec_deployment.main.elasticsearch_username
    password  = ec_deployment.main.elasticsearch_password
  }
}
