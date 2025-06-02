from certifi import contents
from fastapi import APIRouter, HTTPException

from ph_address_api.services.address_services import AddressServices

address_router = APIRouter(
  prefix='/v1/api',
  tags=['Address']
)


@address_router.get('/get-province')
async def get_province(region : str):
  try:
      return await AddressServices.get_provinces_by_region(region)
  except Exception as e:
      print(f'An error occurred: {e}')
      raise e


@address_router.get('/get-cities')
async def get_province(region : str):
    try:
        return await AddressServices.get_cities_by_region(region)
    except Exception as e:
        print(f'An error occurred: {e}')
        raise e

@address_router.get('/get-municipalities')
async def get_province(province : str):
    try:
        return await AddressServices.get_municipalities(province)
    except Exception as e:
        print(f'An error occurred: {e}')
        raise e

