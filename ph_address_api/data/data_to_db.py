import asyncio

from ph_address_api.services.address_services import AddressServices

try:
    """
    This file is for inserting a data in database by calling the functions that 
    I created in the services folder.
    """
    regions_path = 'Regions.csv'
    province_path = 'Province.csv'
    cities = 'Cities.csv'
    muni_path = 'Municipalities.csv'
    brgy_path = 'Barangay.csv'
    # asyncio.run(AddressServices.batch_insert_regions(regions_path))
    # asyncio.run(AddressServices.batch_insert_province_huc(province_path))
    # asyncio.run(AddressServices.batch_insert_cities(cities))
    # asyncio.run(AddressServices.batch_insert_municipalities(muni_path))
    # asyncio.run(AddressServices.batch_insert_brgy(brgy_path))

except Exception as e:
    print(e)




