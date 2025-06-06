
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
        Is a function to insert a batch record in database.
        :param batch: the batch records in a list.
        :return: True, if successfully inserted, otherwise return False.
        """

        #To create a session
        async with create_session() as db:
            try:
                #Insert the batch data
                db.add_all(batch)
                await db.commit()
            except Exception as e:
                # rollback the transactions if encounter error
                await db.rollback()
                print(f'An error occurred: {e}')

    @staticmethod
    async def find_name_by_id(table_name, id, name):
        """
        to find the ids by names.
        :param table_name: the table in db.
        :param id: of the data, that will be inserted.
        :param name: of the data, that will be inserted.
        :return: True, if successfully, otherwise False.
        """
        async with create_session() as db:
            try:
                #the query to select the table where id is equal to the
                # inputted id and the name.
                stmt = (select(table_name).where(
                and_(
                    table_name.id == id,
                    table_name.name == name
                )
                ))
                #execute the query
                result = await db.execute(stmt)
                data = result.scalars().unique().all()
                if not data:
                    return False
                return True
            except Exception as e:
                print(e)
                return False

    @staticmethod
    async def find_name_by_id_in_regions(id, region_name, region_code):
        """
        to find the ids by region name and region code.
        :param id: of the data, that to be inserted.
        :param region_name: of the data, that to be inserted.
        :param region_code: of the data, that to be inserted.
        :return: True, if there's a data, otherwise false
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
        :param table: in db.
        :return: list of id of the specific table.
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
    async def get_all_regions():

        """
        Return all the regions.
        :return: the regions.
        """
        async with create_session() as db:
            try:
                result = await db.execute(select(Regions))
                data = result.scalars().unique().all()
                return data
            except Exception as e:
                raise e
    @staticmethod
    async  def get_provinces_cities(region_name):
        """
        Get provinces names, by inputted region.
        :param region_name: is the user inputted.
        :return: the data, which contains all the provinces names.
        """
        async with create_session() as db:
            try:
                stmt = (select(Regions)
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
    async def get_municipalities(address_name):
        """
        Get Municipalities names.
        :param address_name: is a user inputted. It can be a region or cities or province.
        :return: the list of municipalities.
        """
        async with create_session() as db:
            try:
                stmt = (select(Municipalities)
                        .outerjoin(Province, Province.id == Municipalities.prov_id)
                .outerjoin(City, City.id == Municipalities.city_id)
                .outerjoin(Regions, Regions.id == Municipalities.region_id)
                        .where(or_(Province.name.ilike(address_name),
                                   City.name.ilike(address_name),
                                   Regions.region_name.ilike(address_name),
                                   Regions.region_code.ilike(address_name))))
                result = await db.execute(stmt)
                data = result.scalars().unique().all()
                return data
            except Exception as e:
                raise e

    @staticmethod
    async def get_barangay_in_muni(address_name, municipalities, Table):
        """
        Get the barangay by municipalities and by the parent of the municipalities.
        :param address_name: is the parent of the municipalities.
        :param municipalities: is the name of municipalities.
        :param Table: the name of the table in db.
        :return: the data, which contains all the barangays based on the municipalities and its parent.
        """
        async with create_session() as db:
            try:
                join_1 = (Municipalities.id == Barangay.municipalities_id)
                join_2 = (Regions.id == Municipalities.region_id)
                where_clause = or_(
                    and_(
                        Municipalities.name.ilike(municipalities)
                    ),
                    Regions.region_name.ilike(address_name),
                    Regions.region_code.ilike(address_name)
                )
                if  Table == City:
                    join_1 = (Municipalities.id == Barangay.municipalities_id)
                    join_2 = (City.id == Municipalities.city_id)
                    where_clause = and_(
                        Municipalities.name.ilike(municipalities),
                        City.name.ilike(address_name)
                        )
                elif Table == Province:
                    join_1 = (Municipalities.id == Barangay.municipalities_id)
                    join_2 = (Province.id == Municipalities.prov_id)
                    where_clause = and_(
                        Municipalities.name.ilike(municipalities),
                        Province.name.ilike(address_name)
                    )

                #Query
                stmt = (select(Barangay)
                        .outerjoin(Municipalities, join_1)
                        .outerjoin(Table, join_2)
                        .where(where_clause))
                result = await db.execute(stmt)
                data = result.scalars().unique().all()
                return data
            except Exception as e:
                raise e

