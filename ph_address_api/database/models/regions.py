#import the base model
from ph_address_api.database.models.base import  Base
from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship


class Regions(Base):
    __tablename__  = 'regions'

    id : str = Column('id', String, primary_key=True, index=True)
    region_name : str = Column('region_name',String, nullable=True, index=True)
    region_code : str = Column('region_code',String, nullable=True, index=True)
    population : int = Column('population', Integer)
    island_groups: str = Column('island_groups', String, nullable=True)

    prov = relationship('Province', back_populates='region', lazy='selectin')
    city = relationship('City', back_populates='region', lazy='selectin')
    muni = relationship('Municipalities', lazy='selectin')

    def __init__(self, id = '',
                 region_code = '',
                 region_name = '',
                 population = 0,
                 island_groups = '',
        **kw):

        self.id = id
        self.region_code = region_code
        self.region_name = region_name
        self.population = population
        self.island_groups = island_groups

        super().__init__(**kw)

    def to_dict(self) -> dict:
        return dict(
            id = self.id,
            region_name = self.region_name,
            region_code = self.region_code,
            population = self.population,
            island_groups = self.island_groups,
            provinces = [prov.name for prov in self.prov],
            city = [city.name for city in self.city],
            muni = [mun.name for mun in self.muni]
        )


