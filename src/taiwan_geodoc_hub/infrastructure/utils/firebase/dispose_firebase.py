from firebase_admin import delete_app, get_app


def dispose_firebase():
    try:
        delete_app(get_app())
    except Exception:
        pass
