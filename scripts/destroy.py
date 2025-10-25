import os
from dotenv import load_dotenv
from helpers.get_context import get_context
from helpers.preprocess_terraform_resources import preprocess_terraform_resources
from py_utils import destroy_terraform, init_terraform


def destroy():
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

    terraform_dir = os.path.join(os.getcwd(), "src", "terraform")

    context = get_context(os.path.join(os.getcwd(), "config"))

    preprocess_terraform_resources(
        working_dir=terraform_dir,
        context=context,
    )

    terraform = init_terraform(terraform_dir)

    destroy_terraform(
        terraform=terraform,
        var={
            "elasticsearch_settings_yaml_file_path": os.path.join(
                os.getcwd(), "config", "ec", "elasticsearch.yml"
            ),
            "kibana_settings_yaml_file_path": os.path.join(
                os.getcwd(), "config", "ec", "kibana.yml"
            ),
        },
        var_file=os.path.join(os.getcwd(), "config", "main.tfvars"),
    )


if __name__ == "__main__":
    destroy()
