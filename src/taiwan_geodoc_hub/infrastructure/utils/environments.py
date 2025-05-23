from os import getenv, environ


def is_emulating():
    return getenv("FUNCTIONS_EMULATOR") == "true"


def is_testing():
    return "PYTEST_CURRENT_TEST" in environ


def is_developing():
    return is_testing() or is_emulating()
