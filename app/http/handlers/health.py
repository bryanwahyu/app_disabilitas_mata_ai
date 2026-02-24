from fastapi import APIRouter

from app.pkg.resp import success


def create_router() -> APIRouter:
    router = APIRouter(tags=["Health"])

    @router.get("/health")
    async def health():
        return success("ok", {"status": "ok"})

    return router
