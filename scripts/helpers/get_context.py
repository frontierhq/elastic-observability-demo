import json
import os
from pathlib import Path
from helpers.flatten_json import flatten_json


def get_context(config_dir: str,):
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
        }
        # "kibana": {
        #     "data_view": {},
        # },
    }

    elasticsearch_config_dir = Path(os.path.join(config_dir, "elasticsearch"))
    # kibana_config_dir = os.path.join(config_dir, "kibana")

    if os.path.exists(os.path.join(elasticsearch_config_dir, "cluster_settings.json")):
        with open(os.path.join(elasticsearch_config_dir, "cluster_settings.json")) as file:
            data = json.load(file)
            persistent_flat_data = flatten_json(data["persistent"])
            transient_flat_data = flatten_json(data["transient"])
            context["elasticsearch"]["cluster_settings"]["persistent"] = persistent_flat_data
            context["elasticsearch"]["cluster_settings"]["transient"] = transient_flat_data

    for (dirpath, _, filenames) in os.walk(os.path.join(elasticsearch_config_dir, "component_template")):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["component_template"][Path(
                    filename).stem] = data

    for (dirpath, _, filenames) in os.walk(os.path.join(elasticsearch_config_dir, "index_lifecycle")):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["index_lifecycle"][Path(
                    filename).stem] = data

    for (dirpath, _, filenames) in os.walk(os.path.join(elasticsearch_config_dir, "index_template")):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["index_template"][Path(
                    filename).stem] = data

    for (dirpath, _, filenames) in os.walk(os.path.join(elasticsearch_config_dir, "ingest_pipeline")):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["ingest_pipeline"][Path(
                    filename).stem] = data

    for (dirpath, _, filenames) in os.walk(os.path.join(elasticsearch_config_dir, "security_role_mapping")):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["security_role_mapping"][Path(
                    filename).stem] = data

    # for (dirpath, _, filenames) in os.walk(os.path.join(kibana_config_dir, "data_view")):
    #     for filename in filenames:
    #         with open(os.path.join(dirpath, filename)) as file:
    #             data = json.load(file)
    #             context["kibana"]["data_view"][Path(
    #                 filename).stem] = data

    return context


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
