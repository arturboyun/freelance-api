from fastapi import FastAPI, APIRouter

from app.logs import router as logs

app = FastAPI(title="Log Service", debug=True, version="1.0.0", docs_url="/")

router = APIRouter(prefix="/api/v1")
router.include_router(logs.router)

app.include_router(router)
