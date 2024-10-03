resource "elasticstack_elasticsearch_index_lifecycle" "main" {
  for_each = { for i, v in local.index_lifecycle : v.name => v }

  name = each.value.name

  dynamic "hot" {
    for_each = try(each.value.hot, null) != null ? [each.value.hot] : []

    content {
      min_age = try(hot.value.min_age, null)

      dynamic "rollover" {
        for_each = try(hot.value.rollover, null) != null ? [hot.value.rollover] : []

        content {
          max_age                = try(rollover.value.max_age, null)
          max_primary_shard_size = try(rollover.value.max_primary_shard_size, null)
        }
      }

      dynamic "set_priority" {
        for_each = try(hot.value.set_priority, null) != null ? [hot.value.set_priority] : []

        content {
          priority = try(set_priority.value.priority, null)
        }
      }
    }
  }

  dynamic "warm" {
    for_each = try(each.value.warm, null) != null ? [each.value.warm] : []

    content {
      min_age = try(warm.value.min_age, null)

      dynamic "forcemerge" {
        for_each = try(warm.value.forcemerge, null) != null ? [warm.value.forcemerge] : []

        content {
          max_num_segments = try(forcemerge.value.max_num_segments, null)
        }
      }

      dynamic "set_priority" {
        for_each = try(warm.value.set_priority, null) != null ? [warm.value.set_priority] : []

        content {
          priority = try(set_priority.value.priority, null)
        }
      }
    }
  }

  dynamic "cold" {
    for_each = try(each.value.cold, null) != null ? [each.value.cold] : []

    content {
      min_age = try(cold.value.min_age, null)

      dynamic "allocate" {
        for_each = try(cold.value.allocate, null) != null ? [cold.value.allocate] : []

        content {
          number_of_replicas    = try(allocate.value.number_of_replicas, null)
          total_shards_per_node = try(allocate.value.total_shards_per_node, null)
        }
      }

      dynamic "searchable_snapshot" {
        for_each = try(cold.value.searchable_snapshot, null) != null ? [cold.value.searchable_snapshot] : []

        content {
          force_merge_index   = try(searchable_snapshot.value.force_merge_index, null)
          snapshot_repository = try(searchable_snapshot.value.snapshot_repository, null)
        }
      }

      dynamic "set_priority" {
        for_each = try(cold.value.set_priority, null) != null ? [cold.value.set_priority] : []

        content {
          priority = try(set_priority.value.priority, null)
        }
      }
    }
  }

  dynamic "frozen" {
    for_each = try(each.value.frozen, null) != null ? [each.value.frozen] : []

    content {
      min_age = try(frozen.value.min_age, null)

      dynamic "searchable_snapshot" {
        for_each = try(frozen.value.searchable_snapshot, null) != null ? [frozen.value.searchable_snapshot] : []

        content {
          force_merge_index   = try(searchable_snapshot.value.force_merge_index, null)
          snapshot_repository = try(searchable_snapshot.value.snapshot_repository, null)
        }
      }
    }
  }

  dynamic "delete" {
    for_each = try(each.value.delete, null) != null ? [each.value.delete] : []

    content {
      min_age = try(delete.value.min_age, null)

      dynamic "delete" {
        for_each = try(delete.value.delete, null) != null ? [delete.value.delete] : []

        content {
          delete_searchable_snapshot = try(delete.value.delete_searchable_snapshot, null)
        }
      }
    }
  }
}
