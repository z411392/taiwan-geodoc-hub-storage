from taiwan_geodoc_hub.modules.access_managing.constants.roots import roots


def is_root(user_id: str):
    return user_id in roots
