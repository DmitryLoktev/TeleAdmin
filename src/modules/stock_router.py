from typing import Optional
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.models import Stock
from db.requests import get_table, delete_data, change_stock_beer, add_to_stock

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/stock', response_class=HTMLResponse)
async def get_stock(request: Request):
    table = await get_table(Stock)
    sorted_table = sorted(table, key=lambda x: x.num)
    return templates.TemplateResponse("stock.html", {"request": request, "table_data": sorted_table})


@router.post('/stock')
async def add_to_stock_value(num: Optional[int] = None,
                             style: Optional[str] = None,
                             name: Optional[str] = None,
                             quantity: Optional[int] = None, ):
    try:
        await add_to_stock(num, style, name, quantity, Stock)
        return {"message": "Stock data updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/stock/{stock_id}')
async def update_stock_value_put(stock_id: int,
                                 num: Optional[str] = None,
                                 style: Optional[str] = None,
                                 name: Optional[str] = None,
                                 quantity: Optional[int] = None, ):
    try:
        await change_stock_beer(Stock, stock_id, num, style, name, quantity)
        return {"message": "Stock data updated successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/stock/{stock_id}')
async def delete_beer(stock_id: int):
    try:
        await delete_data(stock_id, Stock)
        return {"message": "Stock data deleted successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
