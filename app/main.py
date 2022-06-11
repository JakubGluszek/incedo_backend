import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from app import api
from app.core.config import JWTSettings, settings

if settings.DEBUG:
    origins = [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://0.0.0.0:3000",
        "http://192.168.2.56:3000",
    ]
else:
    origins = ["https://www.incedo.me"]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
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


@AuthJWT.load_config
def get_config():
    jwt_settings = JWTSettings()
    if settings.DEBUG:
        del jwt_settings.authjwt_cookie_domain
    return jwt_settings


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
