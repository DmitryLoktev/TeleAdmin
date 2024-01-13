from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from modules.kitchen_router import router as kitchen_router
from modules.users_router import router as users_router
from modules.stock_router import router as stock_router
from modules.beer_router import router as beer_router
from db.models import async_main

app = FastAPI(title='TeleAdmin')
app.mount("/static", StaticFiles(directory="templates"), name="static")

app.include_router(beer_router, prefix="/beer")
app.include_router(users_router)
app.include_router(kitchen_router)
app.include_router(stock_router)

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():
    await async_main()


@app.get('/', response_class=HTMLResponse)
async def read_main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})





