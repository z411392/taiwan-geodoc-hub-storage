class TenantNotFound(Exception):
    _tenant_id: str

    def __init__(self, /, tenant_id: str):
        self._tenant_id = tenant_id

    def __iter__(self):
        yield "name", __class__.__name__
        yield "tenantId", self._tenant_id
