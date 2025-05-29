#import the base model
from ph_address_api.database.models.base import  Base
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Column, Integer

class Regions(Base):
    __tablename__  = 'regions'

    id : str = Column('id', String, primary_key=True)
    name : str = Column('region_name',String, nullable=False)
    population : int = Column('population', Integer)

