from fastapi import Request
from fastapi.responses import JSONResponse

async def not_found_handler(
    request: Request,
    exc
):

    # HANDLE ONLY 404
    if exc.status_code == 404:

        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Route Not Found",
                "path": request.url.path
            }
        )

    # RETURN ORIGINAL ERROR
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail
        }
    )