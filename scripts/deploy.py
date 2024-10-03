import os
from helpers.apply_terraform import apply_terraform
from helpers.get_env_value import get_env_value
from helpers.get_context import get_context
from helpers.init_terraform import init_terraform
from helpers.preprocess_terraform_resources import preprocess_terraform_resources


def deploy():
    terraform_dir = os.path.join(os.getcwd(), "src", "terraform")

    ec_deployment_name = get_env_value("EC_DEPLOYMENT_NAME")

    context = get_context(os.path.join(os.getcwd(), "config"))

    preprocess_terraform_resources(
        working_dir=terraform_dir,
        context=context,
    )

    terraform = init_terraform(terraform_dir)

    apply_terraform(
        terraform=terraform,
        var={
            "ec_deployment_name": ec_deployment_name,
        },
        # plan_only=True,
    )


if __name__ == "__main__":
    deploy()
