from fastapi import FastAPI

from src.api.v1.api import api_router
from src.core.db import Base, engine


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(
    title="Eisenhour API",
    description="API for managing tasks based on the Eisenhower Matrix.",
    version="0.1.0",
    on_startup=[create_db_and_tables],
)

app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
