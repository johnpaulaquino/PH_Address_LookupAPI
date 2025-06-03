from fastapi import FastAPI
import uvicorn
from ph_address_api.routes.address_route import address_router

from ph_address_api.utils.app_utils import AppUtility, settings

description = '''
This is a public API to get the address in the Philippines, including the 
Regions, Cities/ Municipalities and Barangay. As of now the zip code is not available, 
but I will add it once I got data.
'''
app = FastAPI(
    description=description,
    title='PH Address API',
    lifespan=AppUtility.app_life_span
)

app.include_router(address_router)


if __name__ == '__main__':
    uvicorn.run("app:app", port=settings.PORT, reload=True)