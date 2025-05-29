from sys import path

import pandas as pd
import os

def clean_data():
    #Read the data from Excel file.
    df = pd.read_excel('./PSGC-1Q-2025-Publication-Datafile.xlsx',
                       engine='openpyxl', sheet_name='PSGC')
    #rename the columns
    df = df.rename(columns={"10-digit PSGC" : 'id',
                            'Correspondence Code':'sub_id',
                            'Geographic Level': 'geo_label',
                            '2020 Population': 'population',
                            'Urban / Rural\n(based on 2020 CPH)':'geo_classification'})

    #drop columns
    drop_cols = ['Old names','Income\nClassification',
                        'Unnamed: 9', 'Status' ]

    pd.to_numeric(df['sub_id'])
    for cols in drop_cols:
        if cols in df.columns:
            df = df.drop(columns=cols)

    #set the id's as 0
    region_id = 0
    prov_id = 0
    city_mun_id = 0
        # loop through the maximum index of the dataframe.
    for i in df.index:
        #store the geo_label in
        geo_label = df.at[i, 'geo_label']
        #store the unique ID
        id_ = df.at[i, 'id']
        # store the city class
        city_class = df.at[i, 'City Class']

        #check if geo_label is equal to Reg or Prov or Mun or City or Barangay,
        # then store the id in specific variable.
        if geo_label == 'Reg':
            region_id = id_
        elif geo_label == 'Prov': #Province
            prov_id = id_
            df.at[i, 'sub_id'] = region_id
        elif geo_label in ['Mun']: #Municipality
            city_mun_id = id_
            df.at[i, 'sub_id'] = prov_id
        elif geo_label == 'City' : #City
            city_mun_id = id_
            df.at[i, 'sub_id'] = region_id if city_class in ['HUC', 'ICC'] else prov_id
        elif geo_label == 'SubMun':
            df.at[i, 'sub_id'] = city_mun_id
        else: #Barangay
            df.at[i, 'sub_id'] = city_mun_id

    #convert the ids and foreign key id to str
    df['id'] = df['id'].astype(str)
    df['sub_id'] = df['sub_id'].astype(str)

    #export the cleaned data
    cleaned_df_path = './cleaned_data.csv'
    df.to_csv(cleaned_df_path)
    print('Successfully exported in csv file.')


clean_data()