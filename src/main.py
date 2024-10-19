from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .routers import auth, messages, websocket
from .config import settings


app = FastAPI()
templates = Jinja2Templates(directory="src/templates")
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.mount("/static", StaticFiles(directory="src/static"), name="static")


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(websocket.router, tags=["websocket"])


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

