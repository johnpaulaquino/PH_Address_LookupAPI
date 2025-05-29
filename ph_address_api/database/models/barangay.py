from sqlalchemy import  Column, String, ForeignKey, Integer
from sqlalchemy.orm import Mapped
from ph_address_api.database.models.base import Base

class Barangay(Base):
    __tablename__ = 'barangay'

    id : str = Column('id', String, primary_key=True)
    city_muni_id : str = Column('city_muni_id', String, ForeignKey('city_muni.id'))
    name : str = Column('name', String)
    population  : int = Column('population', Integer)