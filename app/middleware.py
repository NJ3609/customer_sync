import logging
import time
from fastapi import Request


logger = logging.getLogger("customer-sync")


async def logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = (time.perf_counter() - start) * 1000

    logger.info(
        "%s %s -> %s %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
    )
    return response
