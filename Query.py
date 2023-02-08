import json
import pymysql

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

# Wiping the data on the database
cursor.execute("SELECT * FROM cars")

# Fetching all the records from the table
records = cursor.fetchall()

# Looping through the records and printing each record
if not records:
    print('The database is empty')
else:
    for record in records:
        print(record)

# Closing the cursor and connection
cursor.close()
connection.close()
