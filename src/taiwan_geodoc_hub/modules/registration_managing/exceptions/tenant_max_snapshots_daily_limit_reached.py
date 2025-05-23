class TenantMaxSnapshotsDailyLimitReached(Exception):
    _tenant_id: str
    _date: str

    def __init__(
        self,
        /,
        tenant_id: str,
        date: str,
    ):
        self._tenant_id = tenant_id
        self._date = date

    def __iter__(self):
        yield "name", __class__.__name__
        yield "tenantId", self._tenant_id
        yield "date", self._date
