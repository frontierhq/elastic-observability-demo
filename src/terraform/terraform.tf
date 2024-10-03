terraform {
  required_providers {
    ec = {
      source  = "elastic/ec"
      version = "~> 0.12.1"
    }
    elasticstack = {
      source  = "elastic/elasticstack"
      version = "~> 0.11.8"
    }
  }
}
