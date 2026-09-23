import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = structlog.get_logger(__name__)


class HTTPRequestContextMiddleware(BaseHTTPMiddleware):
    """Wraps every HTTP request this service handles. Does four things:

    1. Request correlation — generates a request_id (UUID) per request and
       binds it into structlog's contextvars, so every log line emitted
       anywhere while handling this request (DAL, BLL, api/, even uvicorn's
       own access-log line) automatically carries the same request_id, with
       no explicit passing required.
    2. Automatic request-level observability — logs request_started and
       request_finished at INFO for every endpoint (method, path,
       status_code, duration_ms), with zero per-route logging code needed.
    3. X-Request-ID response header — echoes the same id back to the caller,
       so one HTTP response can be matched to its exact log lines later.
    4. Last-resort exception safety net — logs anything that reaches this
       try/except at CRITICAL with a full traceback, then re-raises.
       app.add_middleware() wraps around FastAPI's exception-handler system,
       so this only ever catches exceptions with no registered handler —
       genuinely unexpected bugs, never a known domain exception, which
       core/exception_handlers.py already caught before this ever runs.

    Named explicitly "HTTP" because BaseHTTPMiddleware only processes ASGI
    scope type "http" — it never runs for WebSocket connections. A future
    WebSocket endpoint would need its own pure-ASGI middleware for the same
    request_id correlation; it would not get it from this class.
    """

    async def dispatch(self, request: Request, call_next):
        structlog.contextvars.clear_contextvars()
        request_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(request_id=request_id)

        start = time.perf_counter()
        logger.info("request_started", method=request.method, path=request.url.path)
        try:
            response = await call_next(request)
        except Exception:
            logger.critical("request_failed", method=request.method, path=request.url.path, exc_info=True)
            raise

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "request_finished",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )
        response.headers["X-Request-ID"] = request_id
        return response
