from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies.auth import CheckTokenDep
from app.dependencies.helpers.auth import create_database
from app.routers import main_router

CORS = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run at startup
    print("Starting up...")
    create_database()

    yield

    # Code to run at shutdown
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(_: CheckTokenDep, item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
