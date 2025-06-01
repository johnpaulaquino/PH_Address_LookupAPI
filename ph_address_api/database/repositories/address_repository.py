
import os

from ph_address_api.database.engine import create_session
from sqlalchemy import select, and_
from ph_address_api.database.models import *
class AddressRepository:



    @staticmethod
    async def batch_insert(batch):
        """
        :param batch: of the csv file that contains the regions only.
        :return: True, if successfully inserted, otherwise return False.
        """

        #To create a session
        async with create_session() as db:
            try:
                #Insert data
                db.add_all(batch)
                await db.commit()
            except Exception as e:
                # rollback the transactions if encounter error
                await db.rollback()
                print(f'An error occurred: {e}')

    @staticmethod
    async def find_name_by_id(table_name, id, name):
        async with create_session() as db:
            try:
                stmt = (select(table_name).where(
                and_(
                    table_name.id == id,
                    table_name.name == name
                )
                ))
                result = await db.execute(stmt)
                data = result.scalars().all()
                if not data:
                    return False
                return True
            except Exception as e:
                print(e)
                return False

    @staticmethod
    async def get_ids(table):
        try:
            async with create_session() as db:
                stmt = select(table.id)
                result = await db.execute(stmt)
                data = result.scalars().all()
                return data
        except Exception as e:
            print(f'An error occurred: {e}')
            return None