import os
from helpers.format_terraform import format_terraform
from jinja2 import Environment, FileSystemLoader
from python_terraform import Terraform


def normalise_resource_name(value):
    return value.replace("-", "_").replace(".", "_").replace("@", "_")


def preprocess_terraform_resources(
        working_dir: str,
        context: dict = {},
):
    print(f"preprocessing terraform resources in '{working_dir}'")
    env = Environment(
        loader=FileSystemLoader(
            searchpath=working_dir,
        ),
        lstrip_blocks=True,
        trim_blocks=True,
    )
    env.filters["normalise_resource_name"] = normalise_resource_name
    for file in os.listdir(working_dir):
        if file.endswith(".j2"):
            template = env.get_template(file)
            with open(os.path.join(working_dir, template.name.replace(".j2", "")), "w") as f:
                f.write(template.render(context).replace('%{', '%%{'))

    terraform = Terraform(working_dir)

    format_terraform(terraform)


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
