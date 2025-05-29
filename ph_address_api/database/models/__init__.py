from ph_address_api.database.models.base import Base
from ph_address_api.database.models.cities_municiplaities import CitiesMunicipalities
from ph_address_api.database.models.barangay import Barangay
from ph_address_api.database.models.regions import Regions


#to make the imports simplified, instead of importing 1 by 1.
__all__ = [
    "Base",
    "Regions",
    "Barangay",
    "CitiesMunicipalities",
]