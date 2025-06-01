from lxml.html.builder import B

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
                            name= str(val['Name']),
                            population= int(val['population'])
                        )
                    is_exist = await AddressRepository.find_name_by_id(Regions,
                                                                       region.id,
                                                                       region.name)
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

