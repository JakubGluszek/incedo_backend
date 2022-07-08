from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app import api
from app.core.config import settings
from app.db.utils import check_db_connected

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_HOST],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
]

app = FastAPI(title=settings.PROJECT_NAME, middleware=middleware)

app.include_router(api.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    if exc.message == "Signature has expired":
        return Response(status_code=403)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.on_event("startup")
async def app_startup():
    check_db_connected()
