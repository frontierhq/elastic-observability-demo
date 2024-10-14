variable "ec_deployment_name" {
  type = string
}

variable "ec_deployment_template_id" {
  type = string
}

variable "ec_deployment_region" {
  type = string
}

variable "ec_deployment_version" {
  type = string
}

variable "elasticsearch_settings_yaml_file_path" {
  type    = string
  default = null
}

variable "kibana_settings_yaml_file_path" {
  type    = string
  default = null
}
