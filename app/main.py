from fastapi import FastAPI, APIRouter

# from app.modules.logs import router as logs
from app.modules.auth import router as auth
from app.modules.users import router as users

app = FastAPI(title="Freelance API", debug=True, version="1.0.0", docs_url="/")

router = APIRouter(prefix="/api/v1")
router.include_router(auth.router)
router.include_router(users.router)

app.include_router(router)
