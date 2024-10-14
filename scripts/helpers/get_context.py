import json
import os
from pathlib import Path


def get_context(config_dir: str,):
    context = {
        "elasticsearch": {
            "component_template": {},
            "index_lifecycle": {},
            "index_template": {},
            "ingest_pipeline": {},
            "security_role_mapping": {},
        }
    }

    for (dirpath, dirnames, filenames) in os.walk(os.path.join(config_dir, "elasticsearch", "component_template")):
        for filename in filenames:
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["component_template"][Path(
                    filename).stem] = data

    for (dirpath, dirnames, filenames) in os.walk(os.path.join(config_dir, "elasticsearch", "index_lifecycle")):
        for filename in filenames:
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["index_lifecycle"][Path(
                    filename).stem] = data

    for (dirpath, dirnames, filenames) in os.walk(os.path.join(config_dir, "elasticsearch", "index_template")):
        for filename in filenames:
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["index_template"][Path(
                    filename).stem] = data

    for (dirpath, dirnames, filenames) in os.walk(os.path.join(config_dir, "elasticsearch", "ingest_pipeline")):
        for filename in filenames:
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["ingest_pipeline"][Path(
                    filename).stem] = data

    for (dirpath, dirnames, filenames) in os.walk(os.path.join(config_dir, "elasticsearch", "security_role_mapping")):
        for filename in filenames:
            with open(os.path.join(dirpath, filename)) as file:
                data = json.load(file)
                context["elasticsearch"]["security_role_mapping"][Path(
                    filename).stem] = data

    return context


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
