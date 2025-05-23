from enum import Enum


class Namespace(str, Enum):
    NIL = "00000000-0000-0000-0000-000000000000"
    Root = "dc94fa91-4fe4-5133-88e1-f6abd22a8d41"  # DNS / "taiwan-geodoc-hub.firebaseapp.com"
    Tenants = "5d9f473a-6006-5d43-8506-00b51a8a0a58"  # root / "tenants"
    Roles = "343a0cbe-ada4-5058-a3d6-fc4135a483a3"  # tenants / "roles"
    Snapshots = "43383f0f-20f0-57e7-a0dd-47ed11d204ab"  # tenants / "snapshots"
    Registrations = (
        "0cf8fbba-74bd-5c76-827f-6aa88ab94ffe"  # snapshots / "registrations"
    )
    Traces = "56db90d7-e9ac-5f40-a356-96945e65877e"  # root / "traces"

    def __str__(self):
        return f"{self.value}"
