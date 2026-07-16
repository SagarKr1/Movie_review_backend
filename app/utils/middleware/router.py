from fastapi import APIRouter , Depends

# ROUTER
from app.routes.admin import router as adminRoute
from app.routes.public import router as publicRoute

# AUTH
from app.utils.auth.auth import admin_auth


router = APIRouter()

# ==========================================
# ADMIN ROUTES
# ==========================================

router.include_router(
    adminRoute,
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(admin_auth)]
)

# ==========================================
# PUBLIC ROUTES
# ==========================================

router.include_router(
    publicRoute,
    prefix="/public",
    tags=["public"]
)