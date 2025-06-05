
from fastapi import APIRouter

from ph_address_api.services.address_services import AddressServices

#to specify the router, that will include later on the main app
address_router = APIRouter(
  prefix='/v1/api',
  tags=['Address']
)


@address_router.get('/get-province')
async def get_province(region : str):
    """
    An endpoint to get the province that are associated in region.
    :param region: is the user input, to get all province that are associated in region.
    :return: The actual province names of the specific regions.
    """
    try:
        return await AddressServices.get_provinces(region)
    except Exception as e:
        print(f'An error occurred: {e}')
        raise e

@address_router.get('/get-cities')
async def get_province(region : str):
    """
    An endpoint to get the cities that are associated in region.
    :param region: is the user input, to get all cities that are associated in region.
    :return: The actual cities names of the specific regions.
    """
    try:
        return await AddressServices.get_cities(region)
    except Exception as e:
        print(f'An error occurred: {e}')
        raise e

@address_router.get('/get-municipalities')
async def get_province(province : str):
    """
    An endpoint to get the municipalities that are associated in province.
    :param province: is the user input, to get all municipalities that are associated in province.
    :return: The actual municipalities names of the specific province.
    """
    try:
        return await AddressServices.get_muncipalities(province)
    except Exception as e:
        print(f'An error occurred: {e}')
        raise e

@address_router.get('/get-barangays')
async def get_province(address_name : str, municipalities : str):
    """
    An endpoint to get the municipalities that are associated in province.
    :param address_name: is the user input. it can be in cities, province and regions.
    :param municipalities: is the user input, that is associated in the barangays.
    :return: The actual barangay names of the specific municipalities and its parent.
    """
    try:
        data = await AddressServices.get_barangays(address_name, municipalities)
        return data
    except Exception as e:
        print(f'An error occurred: {e}')
        raise e
