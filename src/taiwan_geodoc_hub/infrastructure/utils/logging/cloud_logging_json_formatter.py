from logging import Formatter
from datetime import datetime
from json import dumps
from traceback import format_exception
from typing import Optional


class CloudLoggingJSONFormatter(Formatter):
    def format(self, record):
        timestamp = datetime.fromtimestamp(record.created)
        entry = dict(
            name=record.name,
            severity=record.levelname,
            timestamp=f"{timestamp.isoformat()}Z",
            message=record.getMessage(),
        )

        if hasattr(record, "elapsed"):
            elapsed: float = getattr(record, "elapsed")
            entry["elapsed"] = elapsed

        if record.exc_info and isinstance(record.exc_info, tuple):
            entry["error"] = format_exception(*record.exc_info)

        labels = dict()
        if hasattr(record, "userId"):
            user_id: Optional[str] = getattr(record, "userId")
            if user_id:
                labels.update(userId=user_id)

        if hasattr(record, "tenantId"):
            tenant_id: str = getattr(record, "tenantId")
            if tenant_id:
                labels.update(tenantId=tenant_id)

        if hasattr(record, "snapshotId"):
            snapshot_id: str = getattr(record, "snapshotId")
            if snapshot_id:
                labels.update(snapshotId=snapshot_id)

        entry.update(labels=labels)

        return dumps(
            entry,
            ensure_ascii=False,
            indent=4,
        )
