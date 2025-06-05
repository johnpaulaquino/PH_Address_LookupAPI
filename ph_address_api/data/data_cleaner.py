import pandas as pd


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


    #convert the ids into a string datatype
    df['id'] = df['id'].astype(str)
    df['sub_id'] = df['sub_id'].astype(str)

    #drop columns
    drop_cols = ['Old names','Income\nClassification',
                        'Unnamed: 9', 'Status' ]

    #Set the pateros address to LM(Lone Municipalities)
    pateros = df['Name'] == "Pateros"
    df.loc[pateros, 'City Class'] = 'LM'

    #iterate through the drop_cols list.
    for cols in drop_cols:
        if cols in df.columns:
            df = df.drop(columns=cols)

    #set the id's as 0
    region_id = 0
    prov_id = 0
    city_mun_id = 0
    sub_mun_parent_id = 0

    #loop until it reach the end of the data in excel file.
    for i in df.index:
        #get the geo_label every iteration.
        geo_label = df.at[i, 'geo_label']
        # get the id every iteration.
        id_ = df.at[i, 'id']
        # get the city class every iteration.
        city_class = df.at[i, 'City Class']

        # Update tracking variables and set labels
        if geo_label == 'Reg':

            region_id = id_

            sub_mun_parent_id = region_id

        elif geo_label in ['Prov', "SGA"]:
            prov_id = id_
            df.at[i, 'sub_id'] = region_id

        elif geo_label == 'City':
            city_mun_id = id_
            sub_mun_parent_id = city_mun_id

            if city_class == 'HUC':
                df.at[i, 'sub_id'] = region_id
            else:  # CC or ICC
                df.at[i, 'sub_id'] = prov_id

        elif geo_label in ['Mun']:
            city_mun_id = id_
            if city_class == 'LM':
                df.at[i, 'sub_id'] = region_id
            else:
                df.at[i, 'sub_id'] = prov_id

        elif geo_label == 'SubMun':
            city_mun_id =  id_
            df.at[i, 'sub_id'] = sub_mun_parent_id

        else:  # Barangay
            df.at[i, 'sub_id'] = city_mun_id


    #set zeros to all population that has a null values.
    df['population'] = pd.to_numeric(df['population'].astype(str).str.strip(), errors='coerce')
    df['population'] = df['population'].fillna(0)
    df['population'] = df['population'].astype(int)

    # Select data by its corresponding GEO Level and then save it to csv
    regions_groups = (df[df['geo_label'] == "Reg"])
    regions_groups[['region_name', 'region_code']] = regions_groups['Name'].str.extract(r'^(.*?)\s*\((.*?)\)$')

    regions_groups.to_csv('./Regions.csv')

    province_groups = df['geo_label'] == 'Prov'
    province_huc_groups = df[province_groups | (df['geo_label'] == 'SGA')]
    province_huc_groups.to_csv('./Province.csv') # it will send it to the province

    # First create separate filters
    municipalities = (df['geo_label'] == 'Mun')
    sub_municipalities = (df['geo_label'] == 'SubMun')


    # Combine filters with OR (|)
    combined_filter = df[municipalities | sub_municipalities]
    combined_filter.to_csv('./Municipalities.csv')

    cities = df[df['geo_label'].isin(['City'])]
    cities.to_csv('./Cities.csv')

    brgy_groups = df[df['geo_label'].isin(['Bgy'])]
    brgy_groups.to_csv('./Barangay.csv')


#Call the cleand_data function to clean the data and create separated address.
clean_data()
