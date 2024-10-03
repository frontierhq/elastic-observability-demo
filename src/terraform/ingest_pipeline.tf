resource "elasticstack_elasticsearch_ingest_pipeline" "main" {
  for_each = { for i, v in local.ingest_pipelines : v.name => v }

  name        = each.value.name
  description = each.value.description

  processors = each.value.processors
}
