from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from starlette.exceptions import HTTPException as starletteHTTPException

from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.middleware.route_not_found import not_found_handler

from app.utils.middleware.router import router


app = FastAPI(
    title="Movie Review System",
    description="AI Powered movie review system"
)


origins = [

    "http://localhost:3000",

    "http://127.0.0.1:3000",
    
    os.getenv("FRONTEND_URL")

]

app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# ==========================================
# SECURITY HEADERS MIDDLEWARE
# ==========================================

class SecurityHeadersMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):

        response = await call_next(
            request
        )

        # ==========================================
        # SECURITY HEADERS
        # ==========================================

        response.headers[
            "X-Frame-Options"
        ] = "DENY"

        response.headers[
            "X-Content-Type-Options"
        ] = "nosniff"

        response.headers[
            "Referrer-Policy"
        ] = "strict-origin-when-cross-origin"

        response.headers[
            "Permissions-Policy"
        ] = "camera=(), microphone=()"

        response.headers[
            "Content-Security-Policy"
        ] = "default-src 'self'"

        response.headers[
            "Cache-Control"
        ] = "no-store"

        return response

app.add_middleware(
    SecurityHeadersMiddleware
)

# ==========================================
# REGISTER ROUTES
# ==========================================

app.include_router(router)

# ==========================================
# HEALTH TEST
# ==========================================

@app.get("/")
def health_test():

    return {

        "success": True,

        "message":
        "Movie Review System",

        "version": "1.1.0",

        "status": "ACTIVE"
    }
    
# ==========================================
# NOT FOUND HANDLER
# ==========================================

app.add_exception_handler(

    starletteHTTPException,

    not_found_handler
)