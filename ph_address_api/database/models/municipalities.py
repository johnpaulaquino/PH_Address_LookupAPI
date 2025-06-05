from sqlalchemy import  Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ph_address_api.database.models.base import Base

class Municipalities(Base):
    __tablename__ = 'municipalities'

    id : str = Column('id', String, primary_key=True, index=True)
    prov_id : str = Column('prov_id', String,
                           ForeignKey('province.id',ondelete='cascade'),
                           nullable=True)
    city_id : str = Column('city_id', String,
                           ForeignKey('city.id', ondelete='cascade'),
                           nullable=True )
    #This is for Lone Municipality only, like Pateros in NCR.
    region_id : str = Column('region_id', String,
                           ForeignKey('regions.id', ondelete='cascade'),
                           nullable=True)
    name : str = Column('name', String, index=True)
    zip_code : str = Column('zip_code',String, nullable=True)
    population  : int = Column('population', Integer)

    def  __init__(self, id='', prov_id=None,city_id=None, name='', region_id = None
                  ,zip_code ='',  population=0, **kw):
        self.id = id
        self.prov_id = prov_id
        self.city_id = city_id
        self.region_id = region_id
        self.name = name
        self.population = population
        self.zip_code = zip_code

        super().__init__(**kw)

    def to_dict(self):
        return dict(
            id = self.id,
            name = self.name,
            population = self.population,
            zip_code = self.zip_code,
        )