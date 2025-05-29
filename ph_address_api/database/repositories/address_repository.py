from ph_address_api.database.engine import create_session
from sqlalchemy import insert
from ph_address_api.database.models import *
class AddressRepository:



    @staticmethod
    async def insert_address(regions: Regions,
                             cities_muni : CitiesMunicipalities,
                             brgy: Barangay):
        """
        This will add the records in database in specific tables.

        :param regions: the table from database.,
        :param cities_muni: is the object cities or municipalities.
        :param brgy: is the object barangay.
        :return: True, if successfully added, otherwise return False.
        """
        #To create a session
        async with create_session() as db:
            try:
                # insert in table
                db.add_all(regions, cities_muni, brgy)
                # commit the transactions
                await db.commit()
                # refresh the table
                await db.refresh(regions)

                return True
            except Exception as e:
                # rollback the transactions if encounter error
                await db.rollback()
                print(f'An error occurred: {e}')
                return False