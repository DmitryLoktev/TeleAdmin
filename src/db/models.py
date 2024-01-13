from datetime import datetime
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import dekabrist_base

engine = create_async_engine(dekabrist_base, echo=True)

async_session = async_sessionmaker(engine)

metadata = MetaData()


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_link: Mapped[str] = mapped_column()
    tg_name: Mapped[str] = mapped_column()
    tg_id: Mapped[str] = mapped_column()
    time_on: Mapped[datetime] = mapped_column()


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    pub: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    tg_name: Mapped[str] = mapped_column()
    tg_link: Mapped[str] = mapped_column()
    tg_id: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    date: Mapped[str] = mapped_column()
    time: Mapped[str] = mapped_column()
    quantity: Mapped[str] = mapped_column()
    wish: Mapped[str] = mapped_column()


class Moskovskaya(Base):
    __tablename__ = 'draftbeer_msk'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    brewery: Mapped[str] = mapped_column()
    abv: Mapped[str] = mapped_column()
    style: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()


class Michurina(Base):
    __tablename__ = 'draftbeer_michurina'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    brewery: Mapped[str] = mapped_column()
    abv: Mapped[str] = mapped_column()
    style: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()


class BottledBeer(Base):
    __tablename__ = 'bottled_beer'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    untpd: Mapped[str] = mapped_column()


class KitchenMich(Base):
    __tablename__ = 'kitchen_mich'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()


class Stock(Base):
    __tablename__ = 'stock'

    id: Mapped[int] = mapped_column(primary_key=True)
    num: Mapped[int] = mapped_column()
    style: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
