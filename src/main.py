from fastapi import FastAPI

from src.api.v1.api import api_router

app = FastAPI(
    title="Eisenhour API",
    description="API for managing tasks based on the Eisenhower Matrix.",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
