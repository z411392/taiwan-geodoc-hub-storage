from firebase_admin import initialize_app, get_app
from firebase_admin.credentials import Certificate
from os import getenv
from re import sub


def boot_firebase():
    try:
        get_app()
    except Exception:
        credential = Certificate(
            dict(
                type="service_account",
                project_id=getenv("PROJECT_ID"),
                private_key=sub(r"\\n", "\n", getenv("PRIVATE_KEY")),
                client_email=getenv("CLIENT_EMAIL"),
                token_uri="https://oauth2.googleapis.com/token",
            )
        )
        initialize_app(
            credential=credential,
            options=dict(
                databaseURL=getenv("DATABASE_URL"),
            ),
        )
