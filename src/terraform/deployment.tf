resource "ec_deployment" "main" {
  name = var.ec_deployment_name

  region                 = var.ec_deployment_region
  version                = var.ec_deployment_version
  deployment_template_id = var.ec_deployment_template_id

  elasticsearch = {
    hot = {
      autoscaling = {}
      size        = "4g"
      zone_count  = 2
    }

    warm = {
      autoscaling = {}
      size        = "2g"
      zone_count  = 2
    }

    cold = {
      autoscaling = {}
      size        = "2g"
      zone_count  = 2
    }

    frozen = {
      autoscaling = {}
      size        = "4g"
      zone_count  = 2
    }

    config = {
      user_settings_yaml = var.elasticsearch_settings_yaml_file_path != null ? file(var.elasticsearch_settings_yaml_file_path) : null
    }
  }

  kibana = {
    size       = "1g"
    zone_count = 1

    config = {
      user_settings_yaml = var.kibana_settings_yaml_file_path != null ? file(var.kibana_settings_yaml_file_path) : null
    }
  }
}
