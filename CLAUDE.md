# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository automates Elastic Cloud infrastructure deployment using a **config-as-code + Jinja2 templating** approach. Elasticsearch resources (ingest pipelines, index templates, ILM policies, etc.) are stored as JSON files in `config/elasticsearch/`, then rendered into Terraform resources via Jinja2 templates at deployment time.

## Architecture

### Configuration-to-Terraform Pipeline

The deployment flow follows this architecture:

1. **Configuration Storage** (`config/elasticsearch/`)
   - Each Elasticsearch resource type has its own subdirectory
   - Resources stored as individual JSON files (e.g., `frontier-logs@default.json`)
   - Naming convention: All resources prefixed with `frontier-*`

2. **Context Building** (`scripts/helpers/get_context.py`)
   - Walks `config/elasticsearch/` directories
   - Loads all JSON files into a unified context dictionary
   - Structure: `context["elasticsearch"]["<resource_type>"]["<resource_name>"]`
   - Special handling: cluster_settings are flattened using `flatten_json()`

3. **Terraform Generation** (`scripts/helpers/preprocess_terraform_resources.py`)
   - Renders `.tf.j2` Jinja2 templates → `.tf` files
   - Custom filter: `normalise_resource_name` converts hyphens/dots/@ to underscores
   - Template pattern: Loops over context dict to create Terraform resources
   - Example: `ingest_pipeline.tf.j2` generates one `elasticstack_elasticsearch_ingest_pipeline` resource per pipeline in context

4. **Terraform Apply** (`py_utils` library)
   - Initializes Terraform in `src/terraform/`
   - Applies with vars from `.env` and `config/main.tfvars`

### Bi-directional Sync

**Push**: `make deploy` → Config files → Jinja2 → Terraform → Elasticsearch

**Pull**: `make pull_config` → Elasticsearch API → Compare & write JSON files

The pull script uses two patterns based on API response format:
- **Type 1** (list): `{"component_templates": [{"name": "x", "component_template": {...}}]}`
- **Type 2** (dict): `{"pipeline-name": {...}, "another-pipeline": {...}}`

## Common Commands

```bash
# Development setup
make install                    # Install deps with uv, setup pre-commit

# Deployment workflow
make deploy                     # Deploy all infrastructure and config
make destroy                    # Tear down all infrastructure
make clean                      # Remove .terraform directories

# Configuration sync
make pull_config                # Pull live ES config → local JSON files

# Testing and quality
make test                       # Run all tests (lint + script tests)
make test.lint.python           # Ruff check and format
make test.lint.yaml             # yamllint
make test.script                # Run scripts/test.py
```

## Key Development Patterns

### Adding New Elasticsearch Resources

1. Create JSON file in appropriate `config/elasticsearch/<type>/` directory
2. Follow naming convention: `frontier-<name>.json`
3. Ensure corresponding `.tf.j2` template exists in `src/terraform/`
4. Run `make deploy` - the template will auto-generate Terraform resource

### Modifying Jinja2 Templates

Templates in `src/terraform/*.tf.j2`:
- Loop over `elasticsearch.<resource_type>` dict from context
- Use `normalise_resource_name` filter for Terraform resource names (dashes → underscores)
- Escape Terraform interpolation: template replaces `%{` with `%%{`
- Templates are rendered on every deploy/destroy

### Pulling Live Changes

When someone makes changes directly in Elasticsearch:
1. `make pull_config` fetches resources matching `frontier-*` pattern
2. Compares with existing JSON files (only writes if different)
3. Review changes with `git diff`
4. Commit to source control

### Local Dependency: py-utils

This project depends on `../py-utils` (editable install):
- Provides Terraform wrapper functions: `init_terraform()`, `apply_terraform()`, `destroy_terraform()`
- If modifying Terraform interaction logic, check if changes belong in py-utils

## Important Implementation Details

- **Resource name normalization**: `frontier-logs.rancher@default` → `frontier_logs_rancher_default` for Terraform resource IDs
- **Cluster settings flattening**: Nested cluster settings are flattened to dot notation (e.g., `{"indices": {"recovery": {"max_bytes_per_sec": "100mb"}}}` → `{"indices.recovery.max_bytes_per_sec": "100mb"}`)
- **Environment variables**: Deployment requires `EC_API_KEY` and `EC_DEPLOYMENT_NAME` in `.env`
- **Terraform state**: Stored locally in `src/terraform/terraform.tfstate` (not gitignored)
- **Elastic Cloud deployment**: Uses hot/warm/cold/frozen tiers (see `src/terraform/deployment.tf`)
- **Python 3.11+ required**: Uses modern Python features, managed via uv

## File Reference

Core pipeline components:
- [scripts/deploy.py](scripts/deploy.py) - Orchestrates context → Jinja2 → Terraform → apply
- [scripts/destroy.py](scripts/destroy.py) - Same preprocessing, then Terraform destroy
- [scripts/pull_config.py](scripts/pull_config.py) - Elasticsearch → JSON files
- [scripts/helpers/get_context.py](scripts/helpers/get_context.py) - Build context dict from config/
- [scripts/helpers/preprocess_terraform_resources.py](scripts/helpers/preprocess_terraform_resources.py) - Render Jinja2 templates
- [scripts/helpers/flatten_json.py](scripts/helpers/flatten_json.py) - Flatten nested dicts to dot notation

Configuration locations:
- [config/elasticsearch/](config/elasticsearch/) - All ES resources as JSON
- [config/ec/](config/ec/) - Elasticsearch/Kibana YAML settings (passed to deployment)
- [config/main.tfvars](config/main.tfvars) - Terraform variable values
- [.env](.env) - EC_API_KEY, EC_DEPLOYMENT_NAME (gitignored)

Terraform:
- [src/terraform/deployment.tf](src/terraform/deployment.tf) - EC deployment resource definition
- [src/terraform/*.tf.j2](src/terraform/) - Jinja2 templates that generate ES resource Terraform
- [src/terraform/main.tf](src/terraform/main.tf) - Provider configuration
