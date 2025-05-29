#import the base model
from ph_address_api.database.models.base import  Base
from sqlalchemy import String, Column, Integer, ForeignKey


class Province(Base):
    __tablename__  = 'province'

    id : str = Column('id', String, primary_key=True)
    region_id = Column('region_id', String, ForeignKey('regions.id'))
    name : str = Column('province_name',String, nullable=False)
    population : int = Column('population', Integer)
    island_groups : str = Column('island_groups', String)

