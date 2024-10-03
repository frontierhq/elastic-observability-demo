resource "ec_deployment" "main" {
  name = var.ec_deployment_name

  region                 = var.ec_deployment_region
  version                = var.ec_deployment_version
  deployment_template_id = var.ec_deployment_template_id

  elasticsearch = {
    hot = {
      autoscaling = {}
      size        = "4g"
      zone_count  = 1
    }

    warm = {
      autoscaling = {}
      size        = "2g"
      zone_count  = 1
    }

    cold = {
      autoscaling = {}
      size        = "2g"
      zone_count  = 1
    }

    frozen = {
      autoscaling = {}
      size        = "4g"
      zone_count  = 1
    }
  }

  kibana = {
    size       = "1g"
    zone_count = 1
  }
}
