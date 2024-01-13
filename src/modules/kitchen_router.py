from typing import Optional

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.models import KitchenMich
from db.requests import change_kitchen, add_to_kitchen, delete_data
from fastapi import APIRouter, Request, HTTPException

from db.requests import get_table

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/kitchen', response_class=HTMLResponse)
async def kitchen(request: Request):
    table = await get_table(KitchenMich)
    return templates.TemplateResponse("mich_kitchen.html", {"request": request, "table_data": table})


@router.delete('/kitchen/{kitchen_id}')
async def delete_kitchen(kitchen_id: int):
    try:
        await delete_data(kitchen_id, KitchenMich)
        return {"message": "Kitchen data deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/kitchen')
async def update_kitchen_value_post(
        name: Optional[str] = None,
        price: Optional[int] = None
):
    try:
        table = KitchenMich
        await add_to_kitchen(name, price, table)
        return {"message": "Kitchen data added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/kitchen/{kitchen_id}')
async def update_kitchen_value_put(
        kitchen_id: int,
        name: Optional[str] = None,
        price: Optional[int] = None
):
    try:
        table = KitchenMich
        await change_kitchen(kitchen_id, name, price, table)
        return {"message": "Kitchen data changed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
