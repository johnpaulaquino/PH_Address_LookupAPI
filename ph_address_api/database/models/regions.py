#import the base model
from ph_address_api.database.models.base import  Base
from sqlalchemy import String, Column, Integer

class Regions(Base):
    __tablename__  = 'regions'

    id : str = Column('id', String, primary_key=True, index=True)
    name : str = Column('name',String, nullable=True, index=True)
    population : int = Column('population', Integer)
    island_groups: str = Column('island_groups', String, nullable=True)

    def __init__(self, id = '', name = '',
                 population = 0,
                 island_groups = '',
        **kw):

        self.id = id
        self.name = name
        self.population = population
        self.island_groups = island_groups

        super().__init__(**kw)

    def to_dict(self) -> dict:
        return dict(
            id = self.id,
            name = self.name,
            population = self.population,
            island_groups = self.island_groups
        )


