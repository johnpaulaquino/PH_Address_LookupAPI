from ph_address_api.database.engine import engine
from ph_address_api.database.models import Base


import asyncio

#Create all tables
async def create_tables():
    async with engine.begin() as db:
        try:
            await db.run_sync(Base.metadata.create_all)
        except Exception as e:
            raise e

#Create specific tables
async def create_table(table_name):
    async with engine.begin() as db:
        try:
            await db.run_sync(table_name.metadata.create_all)
        except Exception as e:
            raise e

#Drop all tables
async def drop_tables():
    async with engine.begin() as db:
        try:
            await db.run_sync(Base.metadata.drop_all)
        except Exception as e:
            raise e

#Drop Specific table
async def drop_table(table_name):
    async with engine.begin() as db:
        try:
            await db.run_sync(table_name.__table__.drop)
        except Exception as e:
            raise e

#Call the function to create or drop a table(s) in db
try:
    asyncio.run(create_tables())
except Exception as e:
    print(e)