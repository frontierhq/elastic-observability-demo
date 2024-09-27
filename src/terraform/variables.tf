variable "ec_deployment_name" {
  type = string
}

variable "ec_deployment_template_id" {
  type    = string
  default = "aws-storage-optimized"
}

variable "ec_deployment_region" {
  type    = string
  default = "aws-eu-west-2"
}

variable "ec_deployment_version" {
  type    = string
  default = "8.15.1"
}
