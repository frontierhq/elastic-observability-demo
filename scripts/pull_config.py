import json
import os
from elasticsearch import Elasticsearch
from helpers.init_terraform import init_terraform
from pathlib import Path
from typing import Callable


COMPONENT_TEMPLATES_TO_IGNORE = [
    ".alerts-ecs-mappings",
    ".alerts-framework-mappings",
    ".alerts-legacy-alert-mappings",
    ".alerts-ml.anomaly-detection-health.alerts-mappings",
    ".alerts-ml.anomaly-detection.alerts-mappings",
    ".alerts-observability.apm.alerts-mappings",
    ".alerts-observability.logs.alerts-mappings",
    ".alerts-observability.metrics.alerts-mappings",
    ".alerts-observability.slo.alerts-mappings",
    ".alerts-observability.threshold.alerts-mappings",
    ".alerts-observability.uptime.alerts-mappings",
    ".alerts-security.alerts-mappings",
    ".alerts-stack.alerts-mappings",
    ".alerts-technical-mappings",
    ".alerts-transform.health.alerts-mappings",
    ".deprecation-indexing-mappings",
    ".deprecation-indexing-settings",
    ".fleet_agent_id_verification-1",
    ".fleet_globals-1",
    ".kibana-data-quality-dashboard-ecs-mappings",
    ".kibana-data-quality-dashboard-results-mappings",
    ".kibana-elastic-ai-assistant-component-template-anonymization-fields",
    ".kibana-elastic-ai-assistant-component-template-attack-discovery",
    ".kibana-elastic-ai-assistant-component-template-conversations",
    ".kibana-elastic-ai-assistant-component-template-knowledge-base",
    ".kibana-elastic-ai-assistant-component-template-prompts",
    ".kibana-observability-ai-assistant-component-template-conversations",
    ".kibana-observability-ai-assistant-component-template-kb",
    ".preview.alerts-security.alerts-mappings",
    ".slo-observability.sli-mappings",
    ".slo-observability.sli-settings",
    ".slo-observability.summary-mappings",
    ".slo-observability.summary-settings",
    "apm-10d@lifecycle",
    "apm-180d@lifecycle",
    "apm-390d@lifecycle",
    "apm-90d@lifecycle",
    "apm@mappings",
    "apm@settings",
    "behavioral_analytics-events-mappings",
    "behavioral_analytics-events-settings",
    "data-streams-mappings",
    "data-streams@mappings",
    "ecs@dynamic_templates",
    "ecs@mappings",
    "elastic-connectors-mappings",
    "elastic-connectors-settings",
    "elastic-connectors-sync-jobs-mappings",
    "elastic-connectors-sync-jobs-settings",
    "entities_v1_entity",
    "entities_v1_event",
    "entities_v1_history_base",
    "entities_v1_latest_base",
    "kibana-reporting@custom",
    "kibana-reporting@settings",
    "logs-apm.app-fallback@lifecycle",
    "logs-apm.error-fallback@lifecycle",
    "logs-apm.error@mappings",
    "logs-apm@settings",
    "logs-mappings",
    "logs-settings",
    "logs@mappings",
    "logs@settings",
    "metrics-apm.app-fallback@lifecycle",
    "metrics-apm.internal-fallback@lifecycle",
    "metrics-apm.service_destination.10m-fallback@lifecycle",
    "metrics-apm.service_destination.1m-fallback@lifecycle",
    "metrics-apm.service_destination.60m-fallback@lifecycle",
    "metrics-apm.service_destination@mappings",
    "metrics-apm.service_summary.10m-fallback@lifecycle",
    "metrics-apm.service_summary.1m-fallback@lifecycle",
    "metrics-apm.service_summary.60m-fallback@lifecycle",
    "metrics-apm.service_summary@mappings",
    "metrics-apm.service_transaction.10m-fallback@lifecycle",
    "metrics-apm.service_transaction.1m-fallback@lifecycle",
    "metrics-apm.service_transaction.60m-fallback@lifecycle",
    "metrics-apm.service_transaction@mappings",
    "metrics-apm.transaction.10m-fallback@lifecycle",
    "metrics-apm.transaction.1m-fallback@lifecycle",
    "metrics-apm.transaction.60m-fallback@lifecycle",
    "metrics-apm.transaction@mappings",
    "metrics-apm@mappings",
    "metrics-apm@settings",
    "metrics-mappings",
    "metrics-settings",
    "metrics-tsdb-settings",
    "metrics@mappings",
    "metrics@settings",
    "metrics@tsdb-settings",
    "synthetics-browser.network@package",
    "synthetics-browser.screenshot@package",
    "synthetics-browser@package",
    "synthetics-http@package",
    "synthetics-icmp@package",
    "synthetics-mappings",
    "synthetics-settings",
    "synthetics-tcp@package",
    "synthetics@mappings",
    "synthetics@settings",
    "traces-apm-fallback@lifecycle",
    "traces-apm.rum-fallback@lifecycle",
    "traces-apm.rum@mappings",
    "traces-apm.sampled-fallback@lifecycle",
    "traces-apm@mappings",
    "traces@mappings",
]

INDEX_LIFECYCLES_TO_IGNORE = [
    ".alerts-ilm-policy",
    ".deprecation-indexing-ilm-policy",
    ".fleet-actions-results-ilm-policy",
    ".fleet-file-fromhost-data-ilm-policy",
    ".fleet-file-fromhost-meta-ilm-policy",
    ".fleet-file-tohost-data-ilm-policy",
    ".fleet-file-tohost-meta-ilm-policy",
    ".monitoring-8-ilm-policy",
    ".preview.alerts-security.alerts-policy",
    "180-days-default",
    "180-days@lifecycle",
    "30-days-default",
    "30-days@lifecycle",
    "365-days-default",
    "365-days@lifecycle",
    "7-days-default",
    "7-days@lifecycle",
    "90-days-default",
    "90-days@lifecycle",
    "ilm-history-ilm-policy",
    "kibana-reporting",
    "logs",
    "logs@lifecycle",
    "metrics",
    "metrics@lifecycle",
    "ml-size-based-ilm-policy",
    "slm-history-ilm-policy",
    "synthetics-synthetics.browser-default_policy",
    "synthetics-synthetics.browser_network-default_policy",
    "synthetics-synthetics.browser_screenshot-default_policy",
    "synthetics-synthetics.http-default_policy",
    "synthetics-synthetics.icmp-default_policy",
    "synthetics-synthetics.tcp-default_policy",
    "synthetics",
    "synthetics@lifecycle",
    "watch-history-ilm-policy-16",
]


INDEX_TEMPLATES_TO_IGNORE = [
    ".alerts-default.alerts-default-index-template",
    ".alerts-ml.anomaly-detection-health.alerts-default-index-template",
    ".alerts-ml.anomaly-detection.alerts-default-index-template",
    ".alerts-observability.apm.alerts-default-index-template",
    ".alerts-observability.logs.alerts-default-index-template",
    ".alerts-observability.metrics.alerts-default-index-template",
    ".alerts-observability.slo.alerts-default-index-template",
    ".alerts-observability.threshold.alerts-default-index-template",
    ".alerts-observability.uptime.alerts-default-index-template",
    ".alerts-security.alerts-default-index-template",
    ".alerts-stack.alerts-default-index-template",
    ".alerts-transform.health.alerts-default-index-template",
    ".deprecation-indexing-template",
    ".fleet-fileds-fromhost-data",
    ".fleet-fileds-fromhost-meta",
    ".fleet-fileds-tohost-data",
    ".fleet-fileds-tohost-meta",
    ".kibana-data-quality-dashboard-results-index-template",
    ".kibana-elastic-ai-assistant-index-template-anonymization-fields",
    ".kibana-elastic-ai-assistant-index-template-attack-discovery",
    ".kibana-elastic-ai-assistant-index-template-conversations",
    ".kibana-elastic-ai-assistant-index-template-knowledge-base",
    ".kibana-elastic-ai-assistant-index-template-prompts",
    ".kibana-event-log-template",
    ".kibana-observability-ai-assistant-index-template-conversations",
    ".kibana-observability-ai-assistant-index-template-kb",
    ".kibana-reporting",
    ".ml-anomalies-",
    ".ml-notifications-000002",
    ".ml-state",
    ".ml-stats",
    ".monitoring-beats-mb",
    ".monitoring-ent-search-mb",
    ".monitoring-es-mb",
    ".monitoring-kibana-mb",
    ".monitoring-logstash-mb",
    ".slm-history-7",
    ".slo-observability.sli",
    ".slo-observability.summary",
    ".watch-history-16",
    "apm-source-map",
    "behavioral_analytics-events-default",
    "elastic-connectors-sync-jobs",
    "elastic-connectors",
    "entities_v1_history_index_template",
    "entities_v1_latest_index_template",
    "ilm-history-7",
    "logs-apm.app@template",
    "logs-apm.error@template",
    "logs",
    "metrics-apm.app@template",
    "metrics-apm.internal@template",
    "metrics-apm.service_destination.10m@template",
    "metrics-apm.service_destination.1m@template",
    "metrics-apm.service_destination.60m@template",
    "metrics-apm.service_summary.10m@template",
    "metrics-apm.service_summary.1m@template",
    "metrics-apm.service_summary.60m@template",
    "metrics-apm.service_transaction.10m@template",
    "metrics-apm.service_transaction.1m@template",
    "metrics-apm.service_transaction.60m@template",
    "metrics-apm.transaction.10m@template",
    "metrics-apm.transaction.1m@template",
    "metrics-apm.transaction.60m@template",
    "metrics",
    "search-acl-filter",
    "synthetics-browser",
    "synthetics-browser.network",
    "synthetics-browser.screenshot",
    "synthetics-http",
    "synthetics-icmp",
    "synthetics-tcp",
    "synthetics",
    "traces-apm.rum@template",
    "traces-apm.sampled@template",
    "traces-apm@template",
]


INGEST_PIPELINES_TO_IGNORE = [
    ".fleet_final_pipeline-1",
    ".kibana-elastic-ai-assistant-ingest-pipeline-knowledge-base",
    ".kibana-observability-ai-assistant-kb-ingest-pipeline",
    ".slo-observability.sli.pipeline-v3.3",
    "apm@pipeline",
    "behavioral_analytics-events-final_pipeline",
    "ent-search-generic-ingestion",
    "logs-apm.app@default-pipeline",
    "logs-apm.error@default-pipeline",
    "logs-default-pipeline",
    "logs@default-pipeline",
    "logs@json-message",
    "logs@json-pipeline",
    "metrics-apm.app@default-pipeline",
    "metrics-apm.internal@default-pipeline",
    "metrics-apm.service_destination@default-pipeline",
    "metrics-apm.service_summary@default-pipeline",
    "metrics-apm.service_transaction@default-pipeline",
    "metrics-apm.transaction@default-pipeline",
    "metrics-apm@pipeline",
    "search-default-ingestion",
    "synthetics-browser-1.2.2",
    "synthetics-browser.network-1.2.2",
    "synthetics-browser.screenshot-1.2.2",
    "synthetics-http-1.2.2",
    "synthetics-icmp-1.2.2",
    "synthetics-tcp-1.2.2",
    "traces-apm.rum@default-pipeline",
    "traces-apm@default-pipeline",
    "traces-apm@pipeline",
]

SECURITY_ROLE_MAPPINGS_TO_IGNORE = [
    "elastic-cloud-sso-kibana-do-not-change",
]


def connect():
    terraform_dir = os.path.join(os.getcwd(), "src", "terraform")

    terraform = init_terraform(terraform_dir)
    output = terraform.output()

    return Elasticsearch(
        cloud_id=output["elasticsearch_cloud_id"]["value"],
        basic_auth=(
            output["elasticsearch_username"]["value"],
            output["elasticsearch_password"]["value"],
        )
    )


def delete_keys(obj: dict, keys: list):
    for key in keys:
        del obj[key]


def pull_type_1(fetch: Callable, config_root_dir: str, type: str, ignore_list: list, process: Callable = None):
    result = fetch()

    config_dir = Path(os.path.join(
        config_root_dir,
        "elasticsearch",
        type,
    ))

    for v in result[f"{type}s"]:
        if v["name"] in ignore_list:
            # print(f"Ignoring {type} {v['name']}")
            continue

        config_dir.mkdir(parents=True, exist_ok=True)

        name = v['name']
        file_path = Path(os.path.join(config_dir, f"{name}.json"))

        existing = {}
        if file_path.exists():
            with file_path.open("r") as file:
                existing = json.load(file)

        if process:
            process(v[type])

        if v[type].items() != existing.items():
            with file_path.open("w") as file:
                print(f"Writing {type}/{name} to {file_path}")
                file.write(json.dumps(v[type], indent=2))
                file.write("\n")
        else:
            print(f"Skipping {type}/{name}")


def pull_type_2(fetch: Callable, config_root_dir: str, type: str, ignore_list: list, process: Callable = None):
    result = fetch()

    config_dir = Path(os.path.join(
        config_root_dir,
        "elasticsearch",
        type,
    ))

    for k in result:
        if k in ignore_list:
            # print(f"Ignoring {type} {v['name']}")
            continue

        config_dir.mkdir(parents=True, exist_ok=True)

        name = k
        file_path = Path(os.path.join(config_dir, f"{name}.json"))

        existing = {}
        if file_path.exists():
            with file_path.open("r") as file:
                existing = json.load(file)

        if process:
            process(result[k])

        if result[k].items() != existing.items():
            with file_path.open("w") as file:
                print(f"Writing {type}/{name} to {file_path}")
                file.write(json.dumps(result[k], indent=2))
                file.write("\n")
        else:
            print(f"Skipping {type}/{name}")


def pull_config():
    config_dir = os.path.join(os.getcwd(), "config")

    client = connect()

    pull_type_1(
        lambda: client.cluster.get_component_template(),
        config_dir,
        "component_template",
        COMPONENT_TEMPLATES_TO_IGNORE,
    )
    pull_type_2(
        lambda: client.ilm.get_lifecycle(),
        config_dir,
        "index_lifecycle",
        INDEX_LIFECYCLES_TO_IGNORE,
        lambda x: delete_keys(x, ["in_use_by", "modified_date"]),
    )
    pull_type_1(
        lambda: client.indices.get_index_template(),
        config_dir,
        "index_template",
        INDEX_TEMPLATES_TO_IGNORE,
    )
    pull_type_2(
        lambda: client.ingest.get_pipeline(),
        config_dir,
        "ingest_pipeline",
        INGEST_PIPELINES_TO_IGNORE,
    )
    pull_type_2(
        lambda: client.security.get_role_mapping(),
        config_dir,
        "security_role_mapping",
        SECURITY_ROLE_MAPPINGS_TO_IGNORE,
    )


if __name__ == "__main__":
    pull_config()
