from fastapi import FastAPI

from .api.main import router

app = FastAPI()


app.include_router(router)
