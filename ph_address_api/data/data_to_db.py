from ph_address_api.database.repositories.address_repository import AddressRepository
import asyncio
import pandas as pd

df = pd.read_csv('./cleaned_data.csv')
region_id = 0
city_muni_id = 0
async def insert_data_in_db():
    for i in range(df.index.stop):
        # store the geo_label in variable called geo_label
        geo_label = df.at[i, 'geo_label']
        # store the unique ID in variable, called id_
        id_ = df.at[i, 'id']
        # check if geo_label is equal to Reg or Prov or Mun or City or Barangay,
        # then store the id in specific variable.

        if geo_label == 'Reg':
            region_id = id_
        elif geo_label == 'Prov':  # Province
            prov_id = id_
            df.at[i, 'sub_id'] = region_id
        elif geo_label in ['Mun', 'City']:  # Municipality or city
            mun_id = id_
            df.at[i, 'sub_id'] = city_muni_id if city_muni_id != 0 else region_id
        else:  # Barangay
            df.at[i, 'sub_id'] = mun_id

