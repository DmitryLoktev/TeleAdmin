from typing import Optional
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.models import BottledBeer
from db.requests import get_table, change_beer, change_bottled_beer, delete_data, add_to_bottles
from db import models

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/table/{pub}', response_class=HTMLResponse)
async def get_beer_table(request: Request, pub: str):
    beer_model = getattr(models, pub.capitalize())
    table = await get_table(beer_model)
    return templates.TemplateResponse("beer_table.html", {"request": request, "table_data": table, "pub": pub})


@router.put('/table/{pub}/{beer_id}')
async def change_beer_table(pub: str,
                            beer_id: int,
                            name: Optional[str] = None,
                            brewery: Optional[str] = None,
                            abv: Optional[str] = None,
                            style: Optional[str] = None,
                            price: Optional[str] = None, ):
    try:
        beer_model = getattr(models, pub.capitalize())
        await change_beer(beer_id, name, brewery, abv, style, price, beer_model)
        return {"message": "Tapboard data changed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/bottled', response_class=HTMLResponse)
async def get_bottled_beer(request: Request):
    table = await get_table(BottledBeer)
    return templates.TemplateResponse("bottled.html", {"request": request, "table_data": table})


@router.put('/bottled/{beer_id}')
async def change_bottled_beer_values(beer_id: int,
                                     name: Optional[str] = None,
                                     description: Optional[str] = None,
                                     untpd: Optional[str] = None, ):
    try:
        await change_bottled_beer(BottledBeer, beer_id, name, description, untpd)
        return {"message": "Bottled beer data changed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/bottled/{beer_id}')
async def delete_beer(beer_id: int, session):
    try:
        await delete_data(beer_id, BottledBeer)
        return {"message": "Bottled beer deleted changed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/bottled')
async def new_bottled_beer(request: Request,
                           name: Optional[str] = None,
                           description: Optional[str] = None,
                           untpd: Optional[str] = None, ):
    try:
        await add_to_bottles(name, description, untpd, BottledBeer)
        return {"message": "Bottled beer added successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
