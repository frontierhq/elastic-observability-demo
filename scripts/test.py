import os
from helpers.get_context import get_context
from helpers.preprocess_terraform_resources import preprocess_terraform_resources
from helpers.test_terraform import test_terraform


if __name__ == "__main__":
    terraform_dir = os.path.join(os.getcwd(), "src", "terraform")

    context = get_context(os.path.join(os.getcwd(), "config"))

    preprocess_terraform_resources(
        working_dir=terraform_dir,
        context=context,
    )

    test_terraform(terraform_dir)
