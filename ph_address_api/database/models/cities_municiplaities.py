from sqlalchemy import  Column, String, ForeignKey, Integer
from ph_address_api.database.models.base import Base

class CitiesMunicipalities(Base):
    __tablename__ = 'city_muni'

    id : str = Column('id', String, primary_key=True)
    region_id : str = Column('region_id', String, ForeignKey('regions.id'))
    name : str = Column('name', String)
    zip_code : str = Column('zip_code',String, nullable=True)
    population  : int = Column('population', Integer)