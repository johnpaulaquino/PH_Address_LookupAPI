from openpyxl.drawing import relation
from sqlalchemy import  Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ph_address_api.database.models.base import Base


class City(Base):
    __tablename__ = 'city'

    id : str = Column('id', String, primary_key=True, index=True)
    prov_id : str = Column('prov_id', String,ForeignKey('province.id'), nullable=True)
    region_id : str = Column('region_id', String,ForeignKey('regions.id'), nullable=True)
    name : str = Column('name', String, index=True)
    zip_code : str = Column('zip_code',String, nullable=True)
    population  : int = Column('population', Integer)

    province = relationship('Province', back_populates='cities', lazy='dynamic')
    region = relationship('Regions', back_populates='cities', lazy='dynamic')

    def  __init__(self, id='', prov_id=None,region_id = None, name='',zip_code ='',  population=0, **kw):
        self.id = id
        self.prov_id = prov_id
        self.region_id = region_id
        self.name = name
        self.population = population
        self.zip_code = zip_code

        super().__init__(**kw)