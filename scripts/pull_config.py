import json
import os
from elasticsearch import Elasticsearch
from helpers.init_terraform import init_terraform
from pathlib import Path
from typing import Callable


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


def pull_type_1(fetch: Callable, config_root_dir: str, type: str, process: Callable = None):
    result = fetch()

    config_dir = os.path.join(
        config_root_dir,
        "elasticsearch",
        type,
    )

    ignores = []
    if os.path.exists(os.path.join(config_dir, ".ignore")):
        with open(os.path.join(config_dir, ".ignore")) as file:
            ignores = file.read().splitlines()

    for v in result[f"{type}s"]:
        if v["name"] in ignores:
            # print(f"Ignoring {type} {v['name']}")
            continue

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


def pull_type_2(fetch: Callable, config_root_dir: str, type: str, process: Callable = None):
    result = fetch()

    config_dir = os.path.join(
        config_root_dir,
        "elasticsearch",
        type,
    )

    ignores = []
    if os.path.exists(os.path.join(config_dir, ".ignore")):
        with open(os.path.join(config_dir, ".ignore")) as file:
            ignores = file.read().splitlines()

    for k in result:
        if k in ignores:
            # print(f"Ignoring {type} {v['name']}")
            continue

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
    )
    pull_type_2(
        lambda: client.ilm.get_lifecycle(),
        config_dir,
        "index_lifecycle",
        lambda x: delete_keys(x, ["in_use_by", "modified_date"]),
    )
    pull_type_1(
        lambda: client.indices.get_index_template(),
        config_dir,
        "index_template",
    )
    pull_type_2(
        lambda: client.ingest.get_pipeline(),
        config_dir,
        "ingest_pipeline",
    )
    pull_type_2(
        lambda: client.security.get_role_mapping(),
        config_dir,
        "security_role_mapping",
    )


if __name__ == "__main__":
    pull_config()
