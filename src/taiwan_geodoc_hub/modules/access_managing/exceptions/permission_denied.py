class PermissionDenied(Exception):
    def __init__(self):
        pass

    def __iter__(self):
        yield "name", __class__.__name__
