from fastapi import FastAPI
from .routers import auth, messages, websocket


app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(websocket.router, tags=["websocket"])
