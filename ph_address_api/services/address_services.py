from pyexpat.errors import messages

from fastapi import HTTPException, status
from jinja2.nodes import Add
from starlette.responses import JSONResponse

from ph_address_api.database.models import *
from ph_address_api.database.models.province import Province
from ph_address_api.database.repositories.address_repository import AddressRepository
from csv import DictReader

class AddressServices:

    @staticmethod
    async def batch_insert_regions(file_path: str, batch_size: int = 1000) -> bool:
        try:
            batch = []
            # check the file if it is not scv file, then raise an Exception.
            if not file_path.lower().endswith('.csv'):
                raise Exception('Invalid filetype. Must be a csv file!')

            # then convert the csv into dict
            with (open(file_path, 'r') as file):
                reader = DictReader(file)

                for val in reader:
                    region =  Regions(
                            id = str(val['id']),
                            region_code= str(val['region_code']),
                            region_name= str(val['region_name']),
                            population= int(val['population'])
                        )
                    is_exist = await AddressRepository \
                    .find_name_by_id_in_reginos(
                    region.id,
                    region_name= region.region_name,
                    region_code= region.region_code)

                    if not is_exist:
                        # Append the data in batch
                        batch.append(region)
                    # insert by batch if the length of the batch is
                    # greater than or equal to the batch size.
                    if len(batch) >= batch_size:
                        await AddressRepository.batch_insert(batch)
                        batch = []
                # insert remaining data
                await AddressRepository.batch_insert(batch)
                return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def batch_insert_province_huc(file_path: str, batch_size: int = 1000) -> bool:
        try:
            batch = []
            # check the file if it is not scv file, then raise an Exception.
            if not file_path.lower().endswith('.csv'):
                raise Exception('Invalid filetype. Must be a csv file!')

            # then convert the csv into dict
            with (open(file_path, 'r') as file):
                reader = DictReader(file)

                for val in reader:
                    province = Province(
                        id=str(val['id']),
                        region_id= str(val['sub_id']),
                        name=str(val['Name']),
                        population=int(val['population'])
                    )
                    #if not exist, then append in batch list.
                    is_exist = await AddressRepository.find_name_by_id(Province,
                                                                       province.id,
                                                                       province.name)
                    if not is_exist:
                        # Append the data in batch
                        batch.append(province)
                    # insert by batch if the length of the batch is
                    # greater than or equal to the batch size.
                    if len(batch) >= batch_size:
                        await AddressRepository.batch_insert(batch)
                        batch = []
                # insert remaining data
                if batch:
                    await AddressRepository.batch_insert(batch)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def batch_insert_cities(file_path: str, batch_size: int = 1000):
        try:
            batch = []
            # check the file if it is not scv file, then raise an Exception.
            if not file_path.lower().endswith('.csv'):
                raise Exception('Invalid filetype. Must be a csv file!')

            regions_ids = await AddressRepository.get_ids(Regions)
            # then convert the csv into dict
            with (open(file_path, 'r') as file):
                reader = DictReader(file)

                for val in reader:
                    id = str(val['id'])
                    fk_id = str(val['sub_id'])
                    name = str(val['Name'])
                    population = int(val['population'])


                    if fk_id in regions_ids:
                        city = City(
                            id=id,
                            region_id=fk_id,
                            name=name,
                            population=population)
                    else:
                        city = City(
                            id=id,
                            prov_id=fk_id,
                            name=name,
                            population=population)
                    # if not exist, then append in batch list.
                    is_exist =  await AddressRepository.find_name_by_id(City,
                                                                        city.id,
                                                                        city.name)
                    if not is_exist:
                        # Append the data in batch
                        batch.append(city)
                    # insert by batch if the length of the batch is
                    # greater than or equal to the batch size.
                    if len(batch) >= batch_size:
                        await AddressRepository.batch_insert(batch)
                        batch = []
                # insert remaining data
                if batch:
                    await AddressRepository.batch_insert(batch)

        except Exception as e:
            print(e)

    @staticmethod
    async def batch_insert_municipalities(file_path: str, batch_size: int = 1000):
        try:
            batch = []
            # check the file if it is not scv file, then raise an Exception.
            if not file_path.lower().endswith('.csv'):
                raise Exception('Invalid filetype. Must be a csv file!')

            city_ids = await AddressRepository.get_ids(City)
            region_ids = await AddressRepository.get_ids(Regions)

            # then convert the csv into dict
            with (open(file_path, 'r') as file):
                reader = DictReader(file)

                for val in reader:
                    id = str(val['id'])
                    fk_id = str(val['sub_id'])
                    name = str(val['Name'])
                    population = int(val['population'])

                    if fk_id in city_ids:
                        municipality = Municipalities(
                            id=id,
                            city_id=fk_id,
                            name=name,
                            population=population)
                    else:
                        municipality = Municipalities(
                            id=id,
                            prov_id=fk_id,
                            name=name,
                            population=population)

                    #for Lone municipalities
                    if fk_id in region_ids:
                        municipality = Municipalities(
                            id=id,
                            regions_id=fk_id,
                            name=name,
                            population=population)

                    # if not exist, then append in batch list.
                    is_exist = await AddressRepository.find_name_by_id(Municipalities,
                                                                       municipality.id,
                                                                       municipality.name)
                    if not is_exist:
                        # Append the data in batch
                        batch.append(municipality)
                    # insert by batch if the length of the batch is
                    # greater than or equal to the batch size.
                    if len(batch) >= batch_size:
                        await AddressRepository.batch_insert(batch)
                        batch = []
                # insert remaining data
                if batch:
                    await AddressRepository.batch_insert(batch)

        except Exception as e:
            print(e)

    @staticmethod
    async def batch_insert_brgy(file_path: str, batch_size: int = 1000):
        try:
            batch = []
            # check the file if it is not scv file, then raise an Exception.
            if not file_path.lower().endswith('.csv'):
                raise Exception('Invalid filetype. Must be a csv file!')

            # then convert the csv into dict
            with (open(file_path, 'r') as file):
                reader = DictReader(file)

                city_ids = await AddressRepository.get_ids(City)
                for val in reader:
                    id = str(val['id'])
                    fk_id = str(val['sub_id'])
                    name = str(val['Name'])
                    population = val['population']

                    if fk_id in city_ids:
                        brgy = Barangay(
                        id= id,
                        city_id= fk_id,
                        name=name,
                        population=int(population)
                    )
                    else:
                        brgy = Barangay(
                            id=id,
                            municipalities_id=fk_id,
                            name=name,
                            population=int(population)
                        )
                    # if not exist, then append in batch list.
                    is_exist = await AddressRepository.find_name_by_id(Barangay,
                                                                       brgy.id,
                                                                       brgy.name)
                    if not is_exist:
                        # Append the data in batch
                        batch.append(brgy)
                    # insert by batch if the length of the batch is
                    # greater than or equal to the batch size.
                    if len(batch) >= batch_size:
                        await AddressRepository.batch_insert(batch)
                        batch = []
                # insert remaining data
                if batch:
                    await AddressRepository.batch_insert(batch)
        except Exception as e:
            raise e


    #get the data from region
    @staticmethod
    async def get_provinces_by_region(region_name):
        """

        :param region_name: the name of the region.
        :return: data provinces that are associated in the region entered by the user.
        """
        try:
            # check if the user inputted region is matched in data in db.
            data = await AddressRepository.get_regions_by_name_code(region_name)
            #check if data is null, then raise an error, with a status of 404.
            if not data:
                raise HTTPException(
                    detail="Region not found!",
                    status_code= status.HTTP_404_NOT_FOUND
                )
            #otherwise return the provinces data.
            data = await AddressRepository.get_provinces_by_region(region_name)
            provinces = []

            for row in data:
                if row:
                    provinces.append(row.name)

            if not provinces:
                return JSONResponse(
                    content={"message": 'No provinces found!'},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            return JSONResponse(
                content={'status': 'ok',
                         'message': 'Successfully retrieved!',
                         'provinces': provinces},
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            raise e

    @staticmethod
    async def get_cities_by_region(region_name : str):
        """
        To retrieve the cities that are associated in regions
        :param region_name: that will use to find the cities that are associated.
        :return: JSON Response
        """
        try:
            data = await AddressRepository.get_cities_by_region(region_name)
            if not data:
                raise HTTPException(
                    detail='No Region found!',
                    status_code=status.HTTP_404_NOT_FOUND
                )
            cities_name = []
            for val in data:
                if val is not None:
                    cities_name.append(val.name)

            if not cities_name:
                raise HTTPException(
                    detail= 'No cities found!',
                    status_code= status.HTTP_404_NOT_FOUND
                )

            return JSONResponse(
                content={'status': 'ok',
                         'message': 'Successfully retrieved!',
                         'cities' : cities_name},
                status_code= status.HTTP_200_OK
            )
        except Exception as e:
            raise e

    @staticmethod
    async def get_municipalities(address_name: str):
        """
        To retrieve the municipalities that are associated in Province.
        :param address_name: that will use to find the cities that are associated.
        :return: JSON Response
        """
        try:
            by_prove_data = await AddressRepository.get_muni_by_province(address_name)
            # by_cities_data = await AddressRepository.get_submuni_by_cities(address_name)
            muni_name = []
            # submuni_name = []
            if by_prove_data is not None:
                for val in by_prove_data:
                    muni_name.append(val.name)

            if not muni_name:
                raise HTTPException(
                        detail='No Address found!',
                        status_code=status.HTTP_404_NOT_FOUND
                )

            return JSONResponse(
                content={'status': 'ok',
                         'message': 'Successfully retrieved!',
                         'municipalities': muni_name},
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            raise e