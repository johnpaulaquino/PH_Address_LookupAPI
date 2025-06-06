
from fastapi import HTTPException, status
from starlette.responses import JSONResponse

from ph_address_api.database.models import *
from ph_address_api.database.models.province import Province
from ph_address_api.database.repositories.address_repository import AddressRepository
from csv import DictReader

class AddressServices:

    @staticmethod
    async def batch_insert_regions(file_path: str, batch_size: int = 1000) -> bool:
        """
        Batch insertion in region table in database.
        :param file_path:
            The location of the file.
        :param batch_size:
            The specified number of data in batch to be inserted in database.
        :return:
            True, if successfully, otherwise False.
        """
        try:
            batch = []
            # check the file if it is not scv file, then raise an Exception.
            if not file_path.lower().endswith('.csv'):
                raise Exception('Invalid filetype. Must be a csv file!')

            # Read the file and then convert into dictionary using the DictReader object.
            with (open(file_path, 'r') as file):
                reader = DictReader(file)

                #loop though the value in dictionary
                for val in reader:
                    region =  Regions(
                            id = str(val['id']),
                            name=str(val['Name'].strip()),
                            region_code= str(val['region_code'].strip()),
                            region_name= str(val['region_name'].strip()),
                            population= int(val['population'])
                        )
                    #check if the regions is exist, if yes then ignore it, other wise add.
                    is_exist = await AddressRepository \
                    .find_name_by_id_in_regions(
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
        """
        Batch insertion in province table in database.
        :param file_path:
            The location of the file.
        :param batch_size:
            The specified number of data in batch to be inserted in database.
        :return:
            True, if successfully, otherwise False.
        """
        try:

            batch = []
            # check the file if it is not scv file, then raise an Exception.
            if not file_path.lower().endswith('.csv'):
                raise Exception('Invalid filetype. Must be a csv file!')

            # then convert the csv into dict
            with (open(file_path, 'r') as file):
                reader = DictReader(file)

                #Loop through the data in dictionary.
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
                    name = str(val['Name'].strip())
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
                    name = str(val['Name'].strip())
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
                            region_id=fk_id,
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
                    name = str(val['Name'].strip())
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

    @staticmethod
    async def get_regions():
        try:
            data = await AddressRepository.get_all_regions()
            if not data:
                raise HTTPException(
                    detail = 'No Regions found!',
                    status_code= status.HTTP_404_NOT_FOUND
                )

            regions = [dat.name  for dat in data]

            return JSONResponse(
                content={'status': 'ok',
                         'message': 'Successfully retrieved!',
                         'regions': regions},
                status_code=status.HTTP_200_OK
            )


        except Exception as e:
            print(f'An error occurred: {e}')

    @staticmethod
    async def get_provinces(region_name):
        """
        get province names that are associated in the region.
        :param region_name: the name of the region.
        :return: data provinces that are associated in the region entered by the user.
        """
        try:
            # check if the user inputted region is matched in data in db.
            data = await AddressRepository.get_provinces_cities(region_name)
            #check if data is null, then raise an error, with a status of 404.
            if not data:
                raise HTTPException(
                    detail="Region not found!",
                    status_code= status.HTTP_404_NOT_FOUND
                )
            provinces = data.to_dict()['provinces']

            if not provinces:
                return JSONResponse(
                    content={"message": 'No provinces found!'},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # return json response
            return JSONResponse(
                content={'status': 'ok',
                         'message': 'Successfully retrieved!',
                         'provinces':provinces},
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            raise e

    @staticmethod
    async def get_cities(region_name : str):
        """
               :param region_name: the name of the region.
               :return: data provinces that are associated in the region entered by the user.
        """
        try:
            # check if the user inputted region is matched in data in db.
            data = await AddressRepository.get_provinces_cities(region_name)
            # check if data is null, then raise an error, with a status of 404.

            if not data:
                raise HTTPException(
                    detail="Region not found!",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            cities = data.to_dict()['city']

            if not cities:
                return JSONResponse(
                    content={"message": 'No Cities found!'},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            return JSONResponse(
                content={'status': 'ok',
                         'message': 'Successfully retrieved!',
                         'cities': cities},
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            raise e

    @staticmethod
    async def get_muncipalities(address_name: str):
        """
        Get the municipalities that are associated in region or city or province.
        :param address_name: is the user inputted, which can be a region or city or province
        :return: the data which contains the municipalities name
        """

        try:
            # check if the user inputted region is matched in data in db.
            data = await AddressRepository.get_municipalities(address_name)

            # check if data is null, then raise an error, with a status of 404.

            if not data:
                raise HTTPException(
                    detail="address not found!",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            #list of all names in municipalities
            data = list(sorted(map(lambda x : x.name, data)))

            return JSONResponse(
                content={'status': 'ok',
                         'message': 'Successfully retrieved!',
                         'municipalities': data},
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            raise e

    @staticmethod
    async def get_barangays(address_name : str, municipalites_name : str):
        """
       To get all barangay that are associated in the municipalities and its parent.
       :param address_name: is the user input, which can be a municipalities or cities 
       which depends on their parent.
       :param municipalites_name: is the user input, which is the municipalities.
       :return: 
        """
        try:
            # check if the user inputted region is matched in data in db.
            province_table = await AddressRepository.get_barangay_in_muni(address_name,
                                                                          municipalites_name,
                                                                          Province)
            city_table = await AddressRepository.get_barangay_in_muni(address_name,
                                                                      municipalites_name, City)
            region_table = await AddressRepository.get_barangay_in_muni(address_name,
                                                                        municipalites_name, Regions)

            # check if data is null, then raise an error, with a status of 404.

            if not province_table and not city_table and not region_table:
                raise HTTPException(
                    detail="address not found!",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # check what table is, then it will get that names of the barangay and store in list.
            if province_table:

                data = list(sorted(map(lambda x: x.name, province_table)))
            elif city_table:

                data = list(sorted(map(lambda x: x.name, city_table)))
            else:
                data = list(sorted(map(lambda x: x.name, region_table)))

            # Then return a Json Response
            return JSONResponse(
                content={'status': 'ok',
                         'message': 'Successfully retrieved!',
                         'barangays': data},
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e