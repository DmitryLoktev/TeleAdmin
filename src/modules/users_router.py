from db.models import Book
from db.requests import get_users_with_unique_names, \
    get_books_table, delete_data
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/users', response_class=HTMLResponse)
async def get_users_unique(request: Request):
    users = await get_users_with_unique_names()
    return templates.TemplateResponse("users.html", {"request": request, "table_data": users})


@router.get('/books', response_class=HTMLResponse)
async def get_books(request: Request):
    books = await get_books_table()
    return templates.TemplateResponse("books.html", {"request": request, "table_data": books})


@router.delete('/books/{book_id}')
async def delete_books(book_id: int):

    try:
        await delete_data(book_id, Book)
        return {"message": "Stock data deleted successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
