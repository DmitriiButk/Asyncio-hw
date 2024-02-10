import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import String, Text, Integer


POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'db_async_postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
engine = create_async_engine(PG_DSN)

Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeopleModel(Base):
    __tablename__ = 'swapi_people'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), unique=True)
    birth_year = mapped_column(String(100))
    films = mapped_column(Text)
    species = mapped_column(Text)
    starships = mapped_column(Text)
    vehicles = mapped_column(Text)
    eye_color = mapped_column(String(100))
    gender = mapped_column(String(100))
    hair_color = mapped_column(String(100))
    height = mapped_column(String(100))
    homeworld = mapped_column(String(100))
    mass = mapped_column(String(100))
    skin_color = mapped_column(String(100))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
