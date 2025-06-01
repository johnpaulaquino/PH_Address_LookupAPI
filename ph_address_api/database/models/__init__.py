from ph_address_api.database.models.base import Base
from ph_address_api.database.models.municipalities import Municipalities
from ph_address_api.database.models.barangay import Barangay
from ph_address_api.database.models.regions import Regions
from ph_address_api.database.models.province import Province
from ph_address_api.database.models.city import City


#to make the imports in entire projects simplified.
__all__ = [
    "Base",
    "Regions",
    "Barangay",
    "Municipalities",
    "Province",
    "City",
]