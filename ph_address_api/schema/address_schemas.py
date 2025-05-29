from pydantic import BaseModel


#For Regions Schemas
class RegionSchemaInput(BaseModel):
    id : str
    name : str
    population : int

#For Cities and Municipalities Schemas
class CitiesMuniSchemaInput(BaseModel):
    id : str
    region_id: str
    name : str
    zip_code : str
    population : int

#For Barangay Schemas
class BarangaySchemaInput(BaseModel):
    id : str
    city_muni_id: str
    name : str
    population : int
