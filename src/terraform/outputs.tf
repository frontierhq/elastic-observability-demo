output "elasticsearch_cloud_id" {
  value = ec_deployment.main.elasticsearch.cloud_id
}

output "elasticsearch_password" {
  value     = ec_deployment.main.elasticsearch_password
  sensitive = true
}

output "elasticsearch_username" {
  value     = ec_deployment.main.elasticsearch_username
  sensitive = true
}
