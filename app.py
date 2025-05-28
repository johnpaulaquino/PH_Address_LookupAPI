from sys import path

import pandas as pd
import os

#Read the data from excel file
df = pd.read_excel('./location-data/PSGC-1Q-2025-Publication-Datafile.xlsx',
                   engine='openpyxl', sheet_name='PSGC')
#rename the columns
df = df.rename(columns={"10-digit PSGC" : 'id',
                        'Correspondence Code':'sub_id',
                        'Geographic Level': 'geo_label',
                        '2020 Population': 'population',
                        'Urban / Rural\n(based on 2020 CPH)':'geo_classification'})

#drop columns
drop_cols = ['Old names', 'City Class', 'Income\nClassification',
                    'Unnamed: 9', 'Status' ]

for cols in drop_cols:
  if cols in df.columns:
    df = df.drop(columns=cols)

#set the id's as 0
region_id = 0
prov_id = 0
mun_id = 0



# loop with the range of the length of the data
for i in range(df.index.stop):
    #store the geo_label in variable called geo_label
  geo_label = df.at[i, 'geo_label']
#store the unique ID in variable, called id_
  id_ = df.at[i, 'id']

#check if geo_label is equal to Reg or Prov or Mun or City or Barangay,
    # then store the id in specific variable.
  if geo_label == 'Reg':
    region_id = id_
  elif geo_label == 'Prov': #Province
    prov_id = id_
    df.at[i, 'sub_id'] = region_id
  elif geo_label in ['Mun','City']: #Municipality or city
    mun_id = id_
    df.at[i, 'sub_id'] = prov_id if prov_id != 0 else region_id
  else: #Barangay
    df.at[i, 'sub_id'] = mun_id
