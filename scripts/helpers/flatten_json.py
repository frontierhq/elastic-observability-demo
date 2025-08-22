def flatten_json(y):
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + ".")
        else:
            out[name[:-1]] = x

    flatten(y)

    return out


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
