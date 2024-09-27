import os
from helpers.destroy_terraform import destroy_terraform
from helpers.get_env_value import get_env_value
from helpers.get_context import get_context
from helpers.init_terraform import init_terraform
from helpers.preprocess_terraform_resources import preprocess_terraform_resources


def destroy():
    terraform_dir = os.path.join(os.getcwd(), "src", "terraform")

    ec_deployment_name = get_env_value("EC_DEPLOYMENT_NAME")

    context = get_context(os.path.join(os.getcwd(), "config"))

    preprocess_terraform_resources(
        working_dir=terraform_dir,
        context=context,
    )

    terraform = init_terraform(terraform_dir)

    destroy_terraform(
        terraform=terraform,
        var={
            "ec_deployment_name": ec_deployment_name,
            "elasticsearch_assets_path": os.path.join(os.getcwd(), "src", "elasticsearch"),
        },
    )


if __name__ == "__main__":
    destroy()