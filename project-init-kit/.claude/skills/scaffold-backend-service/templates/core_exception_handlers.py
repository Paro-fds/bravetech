from fastapi import FastAPI


def register_exception_handlers(app: FastAPI) -> None:
    """Register one @app.exception_handler(...) per business-level exception
    in core/exceptions.py that should map to a specific HTTP status. This is
    the ONLY place that translates a domain exception to an HTTP response —
    routers in api/ never do try/except for this.

    Worked example, once a real business exception exists:

        @app.exception_handler(DuplicateEmailError)
        async def handle_duplicate_email(request, exc):
            return JSONResponse(status_code=409, content={"detail": "..."})
    """
