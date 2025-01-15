import logging
import structlog


def configure_logging(log_level: str):
    """
    Configure structured logging with structlog.
    """
    logging.basicConfig(level=log_level)
    structlog.configure(
        processors=[
            structlog.processors.KeyValueRenderer(
                key_order=["event", "log_level"],
            )
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
