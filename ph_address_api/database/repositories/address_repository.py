
import os

from markdown_it.rules_block import table

from ph_address_api.database.engine import create_session
from sqlalchemy import select, and_, or_, join,outerjoin
from sqlalchemy.orm import aliased
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
                data = result.scalars().all()
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
                data = result.scalars().all()
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
    async def get_regions_by_name_code(address_name : str):
        """

        :param address_name: name of the address. ex: NCR or National Capitol Region
        :return:
        """
        try:
            async with create_session() as db:
                stmt = select(Regions).where(
                   or_(
                       Regions.region_name == address_name,
                       Regions.region_code == address_name
                   )
                )
                result = await db.execute(stmt)
                data = result.scalars().one()
                #if no found data, return False, otherwise return true.
                if not data:
                    return False
                return True
        except Exception as e:
            print(f'An error occurred: {e}')
            return False

    @staticmethod
    async  def get_provinces_by_region(region_name):
        async with create_session() as db:
            try:
                stmt = (select(Province)
                .select_from(Regions)
                .outerjoin( Province, Regions.id == Province.region_id)
                .where(or_(Regions.region_name == region_name,
                Regions.region_code == region_name)))

                result = await db.execute(stmt)
                data = result.scalars().all()

                return data

            except Exception as e:
                raise e

    @staticmethod
    async def get_cities_by_region(region_name):
        """

        :param region_name: that will use to find the cities.
        :return: cities that are found.
        """
        async with create_session() as db:
            try:
                stmt = (select(City)
                        .select_from(Regions)
                        .outerjoin(City, Regions.id == City.region_id)
                        .where(or_(Regions.region_name == region_name,
                                   Regions.region_code == region_name)))
                result = await db.execute(stmt)
                data = result.scalars().all()
                if not data:
                    return []
                return data

            except Exception as e:
                raise e

    @staticmethod
    async def get_muni_by_province(province_name):
        """
        :param province_name: that will use to find the cities.
        :return: cities that are found.
        """
        async with create_session() as db:
            try:
                join_expr = (
                    outerjoin(Municipalities,
                              Province, Province.id == Municipalities.prov_id)
                    .outerjoin(City, City.id == Municipalities.city_id)
                    #this will fix, it didn't return the municipality by region.
                    .outerjoin  (Regions, Regions.id == Municipalities.region_id)
                )
                stmt = (
                    select(Municipalities)
                    .distinct()
                    .select_from(
                        join_expr
                    )
                    .where(
                        or_(
                            Province.name == province_name,
                            City.name == province_name,
                            Regions.region_code == province_name,
                            Regions.region_name == province_name,
                        )
                    )
                )# No need for or_ if one condition)
                result = await db.execute(stmt)
                data = result.scalars().all()
                if not data:
                    return []
                return data
            except Exception as e:
                raise e

