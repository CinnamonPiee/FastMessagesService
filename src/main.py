from fastapi import FastAPI
from .routers import auth, messages


app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
