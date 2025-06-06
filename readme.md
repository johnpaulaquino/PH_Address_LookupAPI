# 📍 PH Address LookUp API
This is a public API to get specific addresses. It can return the 
addresses, such as returning the provinces, municipalities, cities and barangays.
It builds to dynamically get the address based on its parent. for example
I want to get the barangays in Santa Cruz Laguna. So, to get
that, there is a parent of barangay, which municipalities, and also
it should input the parent of the municipalities, the Laguna.


## ⏺️ Live Server
You can test the API Here -> [Swagger UI](https://ph-address-lookupapi.onrender.com/docs#/)
## 📍 Endpoints

##### 1. This will return all regions

    https://ph-address-lookupapi.onrender.com/v1/api/get-regions

##### 2. This will return all provinces based on the region.
    https://ph-address-lookupapi.onrender.com/v1/api/get-province?region=replace me

##### 3. This will return all cities based on region.
    https://ph-address-lookupapi.onrender.com/v1/api/get-cities?region=ncr

##### 4. This will return all municiaplaities based on the provicne or region or cities.
    https://ph-address-lookupapi.onrender.com/v1/api/get-municipalities?province=replace me

##### 5. This will return all barangays based on municipalities and its parent.
    https://ph-address-lookupapi.onrender.com/v1/api/get-barangays?address_name=replace me&municipalities=replace me



## 📑 Essential Features
1. [x] Get Regions - This will return all the Region names.
2. [x] Get Provinces - This will return Provinces based on the region input.
3. [x] Get Cities - This will return Cities based on the regions input.
4. [x] Get Municipalities - This will return Municipalities based on the Province or Cities or Regions.
    because, some municipality are in the Province and cities and regions.
5. [x] Get Barangay - This will return the Barangays based on the Municipalities and its parent.

## 🔍 Search & Filter
1. [X] Supports case-insensitive. ex. search: (laguna, lAgUnA). Actual data: Laguna


## ➕ Additional Features
1. [x] Will add soon


        


## 📁 Project Structure
├── ph_address_api/ 
    ├──cached/ 
    ├──config/ 
    ├──data/   
    ├──database/ 
        ├──models/
        ├──repositories/
    ├──routes/
    ├──schema/
    ├──utils/
├──.env
├──.gitignore 
├──alembic.ini
├──app.py # the main app
├──readme.md
├──requirements.txt # Contains the required Packages to run the program.
    
## ⚙️Installation

##### 1. clone the repository
    git clone git@github.com:johnpaulaquino/PH_Address_LookupAPI.git

##### 2. cd to the project
    cd PH_Address_LookupAPI

##### 3. Install Required Packages
    pip install -r requiremtents

##### 4. if you don't want to use software for database, then you can simply change the value in ENVIRONMENT to **'dev'** that can be found in config -> settings. Then run this in you terminal command:
    alembic init -t async migration
##### 4. Simply Go to app.py and then run or simply type this in command:
    python app.py

## 🔐 Environment

##### DB_URL - Contains the url of your db. Just simply replace the credentials below:

    postgresql+asyncpg://<you username>:<your password>@localhost:5432/<you database>
##### PORT - Is the local port for uvicorn
    9090

## 📞 Contacts
**✉️ johnpaul.dev72@gmail.com**

🔗 [My LinkedIn Profile](https://www.linkedin.com/in/aquino-john-paul-b1a708356)
 
☎️ **09858204458**


##### NOTE:

That the data I used in this project is came from :
[PSGC Website](https://psa.gov.ph/classification/psgc)