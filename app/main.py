from fastapi import FastAPI, HTTPException, Security, Request
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi.openapi.utils import get_openapi
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
import logging

from typing import Union
from app.routes import projects, tasks
from app.config import API_KEY_NAME
API_KEY = "1234"
API_KEY_NAME = API_KEY_NAME

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")

app = FastAPI(title="Team Task Tracker API", lifespan=lifespan)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")


app.include_router(
    projects.router,
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Security(verify_api_key)]
)
app.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Security(verify_api_key)]
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Team Task Tracker API",
        version="1.0.0",
        description="This API requires an access token in headers.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": API_KEY_NAME,
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"APIKeyHeader": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    logger.warning(f"404 Not Found: {request.url}")
    return JSONResponse(status_code=404, content={"detail": "Resource not found"})

@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc):
    logger.error(f"Database error on {request.url}: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal database error"})


@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI"}

