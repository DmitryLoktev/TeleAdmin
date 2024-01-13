from fastapi import HTTPException
from db.models import async_session, User, Book
from sqlalchemy import select, update, insert, desc, delete, func


async def get_table(table):
    try:
        async with async_session() as session:
            result = await session.execute(select(table))
            tapboard = result.scalars().all()
            return tapboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_data(book_id, table):
    async with async_session() as session:
        await session.execute(delete(table).where(table.id == book_id))
        await session.commit()


async def change_beer(num, name, brewery, abv, style, price, pub):
    async with async_session() as session:
        statement = (
            update(pub)
            .where(pub.id == num)
            .values(name=name, brewery=brewery, abv=abv, style=style, price=price)
        )
        await session.execute(statement)
        await session.commit()


async def change_kitchen(num, name, price, kitchen_table):
    async with async_session() as session:
        statement = (
            update(kitchen_table)
            .where(kitchen_table.id == num)
            .values(name=name, price=price)
        )
        await session.execute(statement)
        await session.commit()


async def add_to_kitchen(name, price, kitchen_table):
    async with async_session() as session:
        statement = insert(kitchen_table).values(name=name, price=price)
        await session.execute(statement)
        await session.commit()


async def add_to_stock(num, style, name, quantity, table):
    async with async_session() as session:
        statement = insert(table).values(num=num, style=style, name=name, quantity=quantity)
        await session.execute(statement)
        await session.commit()


async def add_to_bottles(name, description, untpd, table):
    async with async_session() as session:
        statement = insert(table).values(name=name, description=description, untpd=untpd)
        await session.execute(statement)
        await session.commit()


async def change_bottled_beer(table, num, name, description, untpd):
    async with async_session() as session:
        statement = (
            update(table)
            .where(table.id == num)
            .values(name=name, description=description, untpd=untpd)
        )
        await session.execute(statement)
        await session.commit()


async def change_stock_beer(table, stock_id, num, style, name, quantity):
    async with async_session() as session:
        statement = (
            update(table)
            .where(table.id == stock_id)
            .values(num=num, style=style, name=name, quantity=quantity)
        )
        await session.execute(statement)
        await session.commit()


async def get_users_with_unique_names():
    try:
        async with async_session() as session:
            stmt = select(User).distinct(User.tg_id).group_by(User.tg_id).order_by(func.max(User.time_on).desc())
            result = await session.execute(stmt)
            unique_users = result.scalars().all()
            return unique_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_books_table():
    try:
        async with async_session() as session:

            result = await session.execute(select(Book).order_by(desc(Book.id)))
            books = result.scalars().all()
            return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
