from sqlalchemy import  Column, String, ForeignKey, Integer
from ph_address_api.database.models.base import Base

class Barangay(Base):
    __tablename__ = 'barangay'

    id : str = Column('id', String, primary_key=True, index=True)
    city_id : str = Column('city_id', String,
                                ForeignKey('city.id',
                                           ondelete='cascade'), nullable=True)
    municipalities_id: str = Column('municipalities_id', String,
                          ForeignKey('municipalities.id',
                                     ondelete='cascade'), nullable=True)
    name: str = Column('name', String, index=True)
    population  : int = Column('population', Integer)


    def __init__(self, id = '', city_id = None,
                 municipalities_id =None, name= '',
                 population = 0, **kw):
        self.id = id
        self.city_id = city_id
        self.municipalities_id = municipalities_id
        self.name = name
        self.population = population
        super().__init__(**kw)