from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse

base_router = APIRouter()

@base_router.get("/", include_in_schema=False)
@base_router.get("/docs", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/api/docs", status_code=status.HTTP_308_PERMANENT_REDIRECT)