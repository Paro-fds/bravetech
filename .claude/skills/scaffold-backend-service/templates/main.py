from fastapi import FastAPI

from app.api import v1
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import HTTPRequestContextMiddleware

configure_logging(settings.log_level, settings.environment)

app = FastAPI(title="{{SERVICE_TITLE}}")
app.add_middleware(HTTPRequestContextMiddleware)
register_exception_handlers(app)

app.include_router(v1.router, prefix="/api/v1")

# If a browser-based frontend on a different origin will call this service,
# add CORSMiddleware here now, with the allowed origin(s) as a Settings
# field — not hardcoded. curl-based verification cannot catch a missing
# CORS config; only a real browser-based check can. See
# project-docs/learnings/03-backend-layered-architecture-template.md.
