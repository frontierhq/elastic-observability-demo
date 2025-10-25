import json
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, NotFoundError
from pathlib import Path
from py_utils import init_terraform
from typing import Callable


NAME_PATTERNS = "frontier-*"


def connect():
    terraform_dir = os.path.join(os.getcwd(), "src", "terraform")

    terraform = init_terraform(terraform_dir)
    output = terraform.output()

    return Elasticsearch(
        cloud_id=output["elasticsearch_cloud_id"]["value"],
        basic_auth=(
            output["elasticsearch_username"]["value"],
            output["elasticsearch_password"]["value"],
        ),
    )


def delete_keys(obj: dict, keys: list):
    for key in keys:
        del obj[key]


def pull_type_1(
    fetch: Callable, config_root_dir: str, type: str, process: Callable = None
):
    try:
        result = fetch()
    except NotFoundError:
        result = {f"{type}s": []}

    config_dir = Path(
        os.path.join(
            config_root_dir,
            "elasticsearch",
            type,
        )
    )

    for v in result[f"{type}s"]:
        config_dir.mkdir(parents=True, exist_ok=True)

        name = v["name"]
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


def pull_type_2(
    fetch: Callable, config_root_dir: str, type: str, process: Callable = None
):
    try:
        result = fetch()
    except NotFoundError:
        result = {}

    config_dir = Path(
        os.path.join(
            config_root_dir,
            "elasticsearch",
            type,
        )
    )

    for k in result:
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
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

    config_dir = os.path.join(os.getcwd(), "config")

    client = connect()

    pull_type_1(
        lambda: client.cluster.get_component_template(name=NAME_PATTERNS),
        config_dir,
        "component_template",
    )
    pull_type_2(
        lambda: client.ilm.get_lifecycle(name=NAME_PATTERNS),
        config_dir,
        "index_lifecycle",
        lambda x: delete_keys(x, ["in_use_by", "modified_date"]),
    )
    pull_type_1(
        lambda: client.indices.get_index_template(name=NAME_PATTERNS),
        config_dir,
        "index_template",
    )
    pull_type_2(
        lambda: client.ingest.get_pipeline(filter_path=NAME_PATTERNS),
        config_dir,
        "ingest_pipeline",
    )
    pull_type_2(
        lambda: client.snapshot.get_repository(filter_path=NAME_PATTERNS),
        config_dir,
        "snapshot_repository",
    )
    pull_type_2(
        lambda: client.security.get_role_mapping(name=NAME_PATTERNS),
        config_dir,
        "security_role_mapping",
    )


if __name__ == "__main__":
    pull_config()
