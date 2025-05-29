from ph_address_api.database.repositories.address_repository import AddressRepository

class AddressServices:

    @staticmethod
    async def insert_address(regions, cities_muni, brgy):
        try:
            await AddressRepository.insert_address(regions,
                                                   cities_muni,
                                                   brgy)
        except Exception as e:
            print(e)