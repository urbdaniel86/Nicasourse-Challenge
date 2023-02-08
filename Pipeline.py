import json
import pandas as pd
import pymysql
from Utils import remove_missing, date_formatting, extract_year, categorical_encoding

# EXTRACT

# Importing CSV source file
df = pd.read_csv('Car_sales.csv')
print('File extraction sucessful, proceeding to transform data')

# TRANSFORM

# Removing rows missing data
df = remove_missing(df)

# Converting the date columns to a standard format
df['Latest_Launch'] = date_formatting(df['Latest_Launch'])

# Creating a new column to store the year of the launch
df['Year_Launch'] = extract_year(df['Latest_Launch'])

# Replacing the categorical values in the "Vehicle_type" column with numerical values
dict_vehicle_type = {'Passenger': 1, 'Car': 2}
df['Vehicle_type'] = categorical_encoding(df['Vehicle_type'],
                                          dict_vehicle_type)

print('Data transformation successful, proceeding to load on the database')

# LOAD

# Creating a surrogate id, so I can verify if records are already in the DB
# It'll be a combination of year, make, and model
df['Car_id'] = df['Year_Launch'].astype(
    str) + '_' + df['Manufacturer'].str.strip() + df['Model'].str.strip()

# Casting float columns to string so they can be loaded to the DB
for column in df.columns:
    if df[column].dtype == 'float64':
        df[column] = df[column].apply(lambda x: '{:.6f}'.format(x))

# Connecting to the database
with open('Credentials.json') as f:
    credentials = json.load(f)

host = credentials['host']
user = credentials['user']
password = credentials['password']
db = credentials['db']

connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=db,
                             port=3306)

cursor = connection.cursor()

# Iterating over the dataframe to insert records
for index, row in df.iterrows():
    sql = '''
    SELECT * FROM cars
    WHERE car_id = %s
    '''
    cursor.execute(sql, (row['Car_id']))
    result = cursor.fetchone()

    # Verifying if the record already exists. If not, it'll be inserted
    if result is None:
        sql = '''
        INSERT INTO cars (car_id,
                          manufacturer,
                          model,
                          sales,
                          resale_value,
                          vehicle_type,
                          price,
                          engine_size,
                          horsepower,
                          wheelbase,
                          width,
                          length,
                          curb_weight,
                          fuel_capacity,
                          fuel_efficiency,
                          latest_launch,
                          power_perf_factor,
                          year_launch)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(sql,
                       (row['Car_id'], row['Manufacturer'], row['Model'],
                        row['Sales_in_thousands'], row['__year_resale_value'],
                        row['Vehicle_type'], row['Price_in_thousands'],
                        row['Engine_size'], row['Horsepower'],
                        row['Wheelbase'], row['Width'], row['Length'],
                        row['Curb_weight'], row['Fuel_capacity'],
                        row['Fuel_efficiency'], row['Latest_Launch'],
                        row['Power_perf_factor'], row['Year_Launch']))
    else:
        print(
            f'The vechicle {row.Car_id} being inserted already exists in the database'
        )

# Commiting the changes
connection.commit()

# Closing the cursor and connection
cursor.close()
connection.close()
print('Data loaded successfully')
