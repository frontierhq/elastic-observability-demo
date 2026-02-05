terraform {
  required_version = "~> 1.11"

  required_providers {
    ec = {
      source  = "elastic/ec"
      version = "~> 0.12.4"
    }
    elasticstack = {
      source  = "elastic/elasticstack"
      version = "~> 0.13.1"
    }
  }
}
