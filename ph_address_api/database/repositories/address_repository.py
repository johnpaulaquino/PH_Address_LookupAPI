
import os

from markdown_it.rules_block import table
from sqlalchemy import func

from ph_address_api.database.engine import create_session
from sqlalchemy import select, and_, or_, join,outerjoin
from sqlalchemy.orm import aliased, joinedload, selectinload
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
        """

        :param table_name: the table in db.
        :param id: of the data, that will be inserted.
        :param name: of the data, that will be inserted.
        :return: True, if successfully, otherwise False.
        """
        async with create_session() as db:
            try:
                stmt = (select(table_name).where(
                and_(
                    table_name.id == id,
                    table_name.name == name
                )
                ))
                result = await db.execute(stmt)
                data = result.scalars().unique().all()
                if not data:
                    return False
                return True
            except Exception as e:
                print(e)
                return False

    @staticmethod
    async def find_name_by_id_in_reginos(id, region_name, region_code):
        """

        :param table_name: the table in db.
        :param id: of the data, that will be inserted.
        :param name: of the data, that will be inserted.
        :return: True, if successfully, otherwise False.
        """
        async with create_session() as db:
            try:
                stmt = (select(Regions).where(
                and_(
                    Regions.id == id,
                    Regions.region_name == region_name,
                    Regions.region_code == region_code
                )
                ))
                result = await db.execute(stmt)
                data = result.scalars().unique().all()
                if not data:
                    return False
                return True
            except Exception as e:
                print(e)
                return False


    @staticmethod
    async def get_ids(table):
        """
        Get all id of specific table.
        :param table: table in db.
        :return: list of id of the speific table.
        """
        try:
            async with create_session() as db:
                stmt = select(table.id)
                result = await db.execute(stmt)
                data = result.scalars().all()
                return data
        except Exception as e:
            print(f'An error occurred: {e}')
            return None

    @staticmethod
    async  def get_provinces_cities(region_name):
        async with create_session() as db:
            try:
                stmt = (select(Regions).options(selectinload(Regions.muni))
                .where(
                    or_( Regions.region_code.ilike(region_name),
                         Regions.region_name.ilike(region_name))

                ))
                result = await db.execute(stmt)
                data = result.unique().scalar_one_or_none()
                return data
            except Exception as e:
                raise e

    @staticmethod
    async def get_municipalities(address_name, Table):
        async with create_session() as db:
            try:
                pass
            except Exception as e:
                raise e

