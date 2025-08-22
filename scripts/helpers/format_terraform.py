from python_terraform import Terraform


def format_terraform(
    terraform: Terraform,
):
    return_code, _, _ = terraform.fmt(
        capture_output=False,
    )
    if return_code != 0:
        exit(return_code)


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
