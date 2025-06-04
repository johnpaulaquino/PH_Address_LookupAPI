from certifi import contents
from fastapi import APIRouter, HTTPException

from ph_address_api.database.models import *
from ph_address_api.database.repositories.address_repository import AddressRepository
from ph_address_api.services.address_services import AddressServices

address_router = APIRouter(
  prefix='/v1/api',
  tags=['Address']
)


@address_router.get('/get-province')
async def get_province(region : str):
  try:
      return await AddressServices.get_provinces(region)
  except Exception as e:
      print(f'An error occurred: {e}')
      raise e

@address_router.get('/get-cities')
async def get_province(region : str):
    try:
        return await AddressServices.get_cities(region)
    except Exception as e:
        print(f'An error occurred: {e}')
        raise e

@address_router.get('/get-municipalities')
async def get_province(province : str):
    try:
        return await AddressServices.get_muncipalities(province)
    except Exception as e:
        print(f'An error occurred: {e}')
        raise e

# @address_router.get('/get-sample')
# async def get_province(province : str):
#     try:
#         data = await AddressRepository.get_barangays(province)
#
#         return data
#     except Exception as e:
#         print(f'An error occurred: {e}')
#         raise e
