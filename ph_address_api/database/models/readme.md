# Models

## Barangay
This model contains columns called:

### **id** 
Is a primary key and unique identification of barangay table.

### city_id
Is a foreign key of **City**, which will use to connect in city table. This can be null,
and it is on delete cascade, means when the parent deleted then it will delete its child.

### municipalities_id
Is a foreign key of **Municipalities**, which will use to connect in municipalities table. This can be null,
and it is on delete cascade, means, when the parent deleted then it will delete its child.

### name
Is a name of the address or location in the philippines.

### population

The total number of population in barangay.



## City
This model contains a columns called:

### id
Is a primary key and unique identification of City table.

### prov_id
Is a foreign key of **province**, which will use to connect in province table. This can be null,
and it is on delete cascade, means when the parent deleted then it will delete its child.

### region_id
Is a foreign key of **regions**, which will use to connect in region table. This can be null,
and it is on delete cascade, means when the parent deleted then it will delete its child.

### name
Is a name of the address or location in the philippines.

### zip_code
Is a Zip code of the City, especially in NCR region.

### population
The total number of population in City.



## Municipalities
This model contains a columns called:

### id
Is a primary key and unique identification of City table.

### city_id
Is a foreign key of **city**, which will use to connect in city table. This can be null,
and it is on delete cascade, means when the parent deleted then it will delete its child.

### prov_id
Is a foreign key of **province**, which will use to connect in province table. This can be null,
and it is on delete cascade, means when the parent deleted then it will delete its child.

### region_id
Is a foreign key of **regions**, which will use to connect in region table. This can be null,
and it is on delete cascade, means when the parent deleted then it will delete its child.

### name
Is a name of the address or location in the philippines.

### zip_code
Is a Zip code of the Municipalities.

### population
The total number of population in Municipality.




## Province
This model contains columns called:

### **id** 
Is a primary key and unique identification of province table.

### region_id
Is a foreign key of **regions**, which will use to connect in region table. This can be null,
and it is on delete cascade, means when the parent deleted then it will delete its child.

### name
Is a name of the address or location in the philippines.

### population
The total number of population in province.

### region
specify the relationship in region. This will also to get all
the data that are associated in region.



## Regions
This model contains columns called:

### **id** 
Is a primary key and unique identification of regions table.

### region_name and region_code
Is a name of the address or location in the philippines.

### population
The total number of population in regions.

### province
specify the relationship in province. This will also to get all
the data that are associated in province.

### city
specify the relationship in city. This will also to get all
the data that are associated in city.