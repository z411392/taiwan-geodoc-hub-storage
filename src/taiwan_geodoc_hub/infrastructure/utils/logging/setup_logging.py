from logging import basicConfig, INFO, WARNING, getLogger, StreamHandler
from taiwan_geodoc_hub.infrastructure.utils.logging.cloud_logging_json_formatter import (
    CloudLoggingJSONFormatter,
)


def setup_logging():
    basicConfig(
        level=INFO,
        format="%(message)s",
        handlers=[StreamHandler()],
    )
    root_logger = getLogger()
    for handler in root_logger.handlers:
        handler.setFormatter(CloudLoggingJSONFormatter())
    getLogger("vellox.lifespan").setLevel(WARNING)
    getLogger("vellox.http").setLevel(WARNING)
    getLogger("werkzeug").setLevel(WARNING)
