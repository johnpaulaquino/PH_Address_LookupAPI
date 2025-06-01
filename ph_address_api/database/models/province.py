#import the base model
from ph_address_api.database.models.base import  Base
from sqlalchemy import String, Column, Integer, ForeignKey


class Province(Base):
    __tablename__  = 'province'

    id : str = Column('id', String, primary_key=True, index=True)
    region_id = Column('region_id', String,
                       ForeignKey('regions.id', ondelete='cascade'))
    name : str = Column('name',String, index=True)
    population : int = Column('population', Integer)

    def __init__(self, id='', region_id='', name='', population=0, **kw):
        self.id = id
        self.region_id = region_id
        self.name = name
        self.population = population
        super().__init__(**kw)


