from importlib import import_module
import os


def import_from_environ():
    dep = os.environ.get("OTEAPI_AUTH_FUNCTION")
    if dep:
        module, dot, funcname = dep.replace(" ", str()).rpartition(".")
        try:
            func = getattr(import_module(module), funcname)
        except Exception as error:
            raise error
    else:
        func = None
    return func