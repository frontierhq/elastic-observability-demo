resource "elasticstack_kibana_data_view" "main" {
  data_view = {
    name            = "logs-*"
    title           = "logs-*"
    time_field_name = "@timestamp"
    namespaces      = []
  }
}
