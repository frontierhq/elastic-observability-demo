from python_terraform import Terraform


def init_terraform(working_dir: str):
    terraform = Terraform(working_dir=working_dir)

    print("initialising terraform")
    return_code, _, _ = terraform.init()
    if (return_code != 0):
        exit(return_code)

    return terraform


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
