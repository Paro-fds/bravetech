"""Structured logging setup (structlog over stdlib).

Python's stdlib logging model has 5 true severities: CRITICAL, ERROR, WARNING,
INFO, DEBUG. "FATAL" and "WARN" are not separate levels — they're just alias
names stdlib itself defines for CRITICAL and WARNING (same integer value).
"TRACE" doesn't exist in stdlib at all; it's registered here, below DEBUG.

Call-site mapping for all six requested levels:
    TRACE (5)     -> logger.log(TRACE, "event_name", **kw)
    DEBUG (10)    -> logger.debug("event_name", **kw)
    INFO (20)     -> logger.info("event_name", **kw)
    WARN (30)     -> logger.warning("event_name", **kw)   -- "warn" is a deprecated stdlib alias, don't use it
    ERROR (40)    -> logger.error("event_name", **kw)
    FATAL (50)    -> logger.critical("event_name", **kw)  -- "fatal" is a deprecated stdlib alias, don't use it

Never pass raw PII as a log field — log an id instead. Check this service's
own data-retention/deletion promises before assuming that's covered.
"""

import logging
import sys

import structlog

TRACE = 5
logging.addLevelName(TRACE, "TRACE")


def configure_logging(log_level: str, environment: str) -> None:
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)

    shared_processors: list = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    renderer = (
        structlog.dev.ConsoleRenderer()
        if environment == "development"
        else structlog.processors.JSONRenderer()
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(log_level)

    # Route uvicorn's own stdlib log records through the same handler/format
    # instead of uvicorn's default config, so everything is one consistent stream.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uv_logger = logging.getLogger(name)
        uv_logger.handlers = []
        uv_logger.propagate = True
