import json
import os
from elasticsearch import Elasticsearch
from helpers.init_terraform import init_terraform


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


def pull_component_templates(client: Elasticsearch, config_dir: str):
    component_template_result = client.cluster.get_component_template(
        name="*@custom",
    )
    for v in component_template_result["component_templates"]:
        file_path = os.path.join(
            config_dir,
            "elasticsearch",
            "component_template",
            f"{v['name']}.json",
        )
        with open(file_path, "w") as file:
            file.write(json.dumps(v["component_template"], indent=2))
            file.write("\n")


def pull_index_lifecycle(client: Elasticsearch, config_dir: str):
    lifecycle_result = client.ilm.get_lifecycle(name="*@custom")
    for k in lifecycle_result:
        file_path = os.path.join(
            config_dir,
            "elasticsearch",
            "index_lifecycle",
            f"{k}.json",
        )
        del lifecycle_result[k]["in_use_by"]
        del lifecycle_result[k]["modified_date"]
        with open(file_path, "w") as file:
            file.write(json.dumps(lifecycle_result[k], indent=2))
            file.write("\n")


def pull_index_template(client: Elasticsearch, config_dir: str):
    index_template_result = client.indices.get_index_template(name="*@custom")
    for v in index_template_result["index_templates"]:
        file_path = os.path.join(
            config_dir,
            "elasticsearch",
            "index_template",
            f"{v['name']}.json",
        )
        with open(file_path, "w") as file:
            file.write(json.dumps(v["index_template"], indent=2))
            file.write("\n")


def pull_ingest_pipeline(client: Elasticsearch, config_dir: str):
    pipeline_result = client.ingest.get_pipeline(filter_path="*@custom")
    for k in pipeline_result:
        file_path = os.path.join(
            config_dir,
            "elasticsearch",
            "ingest_pipeline",
            f"{k}.json",
        )
        with open(file_path, "w") as file:
            file.write(json.dumps(pipeline_result[k], indent=2))
            file.write("\n")


def pull_role_mapping(client: Elasticsearch, config_dir: str):
    role_mapping_result = client.security.get_role_mapping(
        filter_path="*@custom",
    )
    for k in role_mapping_result:
        file_path = os.path.join(
            config_dir,
            "elasticsearch",
            "security_role_mapping",
            f"{k}.json",
        )
        with open(file_path, "w") as file:
            file.write(json.dumps(role_mapping_result[k], indent=2))
            file.write("\n")


def pull_config():
    config_dir = os.path.join(os.getcwd(), "config")

    client = connect()

    pull_component_templates(client, config_dir)
    pull_index_lifecycle(client, config_dir)
    pull_index_template(client, config_dir)
    pull_ingest_pipeline(client, config_dir)
    pull_role_mapping(client, config_dir)


if __name__ == "__main__":
    pull_config()
