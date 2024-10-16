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


def pull_component_templates(client: Elasticsearch, config_root_dir: str):
    result = client.cluster.get_component_template()

    config_dir = os.path.join(
        config_root_dir,
        "elasticsearch",
        "component_template",
    )

    ignores = []
    if os.path.exists(os.path.join(config_dir, ".ignore")):
        with open(os.path.join(config_dir, ".ignore")) as file:
            ignores = file.read().splitlines()

    for v in result["component_templates"]:
        if v["name"] in ignores:
            continue
        file_path = os.path.join(config_dir, f"{v['name']}.json")
        with open(file_path, "w") as file:
            file.write(json.dumps(v["component_template"], indent=2))
            file.write("\n")


def pull_index_lifecycle(client: Elasticsearch, config_root_dir: str):
    result = client.ilm.get_lifecycle()

    config_dir = os.path.join(
        config_root_dir,
        "elasticsearch",
        "index_lifecycle",
    )

    ignores = []
    if os.path.exists(os.path.join(config_dir, ".ignore")):
        with open(os.path.join(config_dir, ".ignore")) as file:
            ignores = file.read().splitlines()

    for k in result:
        if k in ignores:
            continue
        file_path = os.path.join(config_dir, f"{k}.json")
        del result[k]["in_use_by"]
        del result[k]["modified_date"]
        with open(file_path, "w") as file:
            file.write(json.dumps(result[k], indent=2))
            file.write("\n")


def pull_index_template(client: Elasticsearch, config_root_dir: str):
    result = client.indices.get_index_template()

    config_dir = os.path.join(
        config_root_dir,
        "elasticsearch",
        "index_template",
    )

    ignores = []
    if os.path.exists(os.path.join(config_dir, ".ignore")):
        with open(os.path.join(config_dir, ".ignore")) as file:
            ignores = file.read().splitlines()

    for v in result["index_templates"]:
        if v["name"] in ignores:
            continue
        file_path = os.path.join(config_dir, f"{v['name']}.json")
        with open(file_path, "w") as file:
            file.write(json.dumps(v["index_template"], indent=2))
            file.write("\n")


def pull_ingest_pipeline(client: Elasticsearch, config_root_dir: str):
    result = client.ingest.get_pipeline()

    config_dir = os.path.join(
        config_root_dir,
        "elasticsearch",
        "ingest_pipeline",
    )

    ignores = []
    if os.path.exists(os.path.join(config_dir, ".ignore")):
        with open(os.path.join(config_dir, ".ignore")) as file:
            ignores = file.read().splitlines()

    for k in result:
        if k in ignores:
            continue
        file_path = os.path.join(config_dir, f"{k}.json")
        with open(file_path, "w") as file:
            file.write(json.dumps(result[k], indent=2))
            file.write("\n")


def pull_role_mapping(client: Elasticsearch, config_root_dir: str):
    result = client.security.get_role_mapping()

    config_dir = os.path.join(
        config_root_dir,
        "elasticsearch",
        "security_role_mapping",
    )

    ignores = []
    if os.path.exists(os.path.join(config_dir, ".ignore")):
        with open(os.path.join(config_dir, ".ignore")) as file:
            ignores = file.read().splitlines()

    for k in result:
        if k in ignores:
            continue
        file_path = os.path.join(config_dir, f"{k}.json")
        with open(file_path, "w") as file:
            file.write(json.dumps(result[k], indent=2))
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
