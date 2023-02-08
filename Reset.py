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
cursor.execute("DELETE FROM cars")

# Committing the changes to the database
connection.commit()

# Closing the cursor and connection
cursor.close()
connection.close()
print('Data wiped successfully')
