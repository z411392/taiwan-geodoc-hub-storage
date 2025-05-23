from logging import Formatter
from datetime import datetime
from json import dumps


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
            (type, exception, traceback) = record.exc_info
            error = dict(
                type=type.__name__ if type else None,
                message=str(exception) if exception else None,
                traceback=traceback,
            )
            entry["error"] = error

        labels = dict()
        if hasattr(record, "userId"):
            userId: str = getattr(record, "userId")
            labels.update(userId=userId)

        if hasattr(record, "tenantId"):
            tenantId: str = getattr(record, "tenantId")
            labels.update(tenantId=tenantId)

        entry.update(labels=labels)

        return dumps(
            entry,
            ensure_ascii=False,
            indent=4,
        )
