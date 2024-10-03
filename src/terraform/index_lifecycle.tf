resource "elasticstack_elasticsearch_index_lifecycle" "main" {
  for_each = { for i, v in local.index_lifecycle : v.name => v }

  name = each.value.name

  dynamic "hot" {
    for_each = try(each.value.hot, null) != null ? [each.value.hot] : []

    content {
      dynamic "rollover" {
        for_each = try(hot.value.rollover, null) != null ? [hot.value.rollover] : []

        content {
          max_age                = rollover.value.max_age
          max_primary_shard_size = rollover.value.max_primary_shard_size
        }
      }
    }
  }
}
