import json
import os
from pathlib import Path
from helpers.flatten_json import flatten_json


def get_context(
    config_dir: str,
):
    context = {
        "elasticsearch": {
            "cluster_settings": {
                "persistent": {},
                "transient": {},
            },
            "component_template": {},
            "index_lifecycle": {},
            "index_template": {},
            "ingest_pipeline": {},
            "security_role_mapping": {},
            "snapshot_repository": {},
        }
    }

    elasticsearch_config_dir = Path(os.path.join(config_dir, "elasticsearch"))

    if os.path.exists(os.path.join(elasticsearch_config_dir, "cluster_settings.json")):
        with open(
            os.path.join(elasticsearch_config_dir, "cluster_settings.json")
        ) as file:
            data = json.load(file)
            if "persistent" in data:
                persistent_flat_data = flatten_json(data["persistent"])
                context["elasticsearch"]["cluster_settings"]["persistent"] = (
                    persistent_flat_data
                )
            if "transient" in data:
                transient_flat_data = flatten_json(data["transient"])
                context["elasticsearch"]["cluster_settings"]["transient"] = (
                    transient_flat_data
                )

    for dirpath, _, filenames in os.walk(
        os.path.join(elasticsearch_config_dir, "component_template")
    ):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["component_template"][Path(filename).stem] = (
                    data
                )

    for dirpath, _, filenames in os.walk(
        os.path.join(elasticsearch_config_dir, "index_lifecycle")
    ):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["index_lifecycle"][Path(filename).stem] = data

    for dirpath, _, filenames in os.walk(
        os.path.join(elasticsearch_config_dir, "index_template")
    ):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["index_template"][Path(filename).stem] = data

    for dirpath, _, filenames in os.walk(
        os.path.join(elasticsearch_config_dir, "ingest_pipeline")
    ):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["ingest_pipeline"][Path(filename).stem] = data

    for dirpath, _, filenames in os.walk(
        os.path.join(elasticsearch_config_dir, "security_role_mapping")
    ):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["security_role_mapping"][
                    Path(filename).stem
                ] = data

    for dirpath, _, filenames in os.walk(
        os.path.join(elasticsearch_config_dir, "snapshot_repository")
    ):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["snapshot_repository"][Path(filename).stem] = (
                    data
                )

    return context


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
