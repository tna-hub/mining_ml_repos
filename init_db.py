import configparser
import csv

from psycopg2 import connect, extensions, sql

config = configparser.ConfigParser()
config.read('data/db.ini')

host = config['postgresql']['host']
user = config['postgresql']['user']
passwd = config['postgresql']['passwd']
db = config['postgresql']['db']

# declare a new PostgreSQL connection object
conn = connect(
    dbname='postgres',
    user=user,
    host=host,
    password=passwd
)

# get the isolation level for autocommit
autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT

"""
ISOLATION LEVELS for psycopg2
0 = READ UNCOMMITTED
1 = READ COMMITTED
2 = REPEATABLE READ
3 = SERIALIZABLE
4 = DEFAULT
"""

# set the isolation level for the connection's cursors
# will raise ActiveSqlTransaction exception otherwise
conn.set_isolation_level(autocommit)

# instantiate a cursor object from the connection
cursor = conn.cursor()

# use the sql module instead to avoid SQL injection attacks
try:

    cursor.execute(sql.SQL(
        "DROP DATABASE IF EXISTS {};"
    ).format(sql.Identifier(db)))

    cursor.execute(sql.SQL(
        "CREATE DATABASE {};"
    ).format(sql.Identifier(db)))
    # close the cursor to avoid memory leaks
    cursor.close()
    # close the connection to avoid memory leaks
    conn.close()
except Exception as e:
    print(e)
    exit()

# declare a new PostgreSQL connection object
conn = connect(
    dbname=db,
    user=user,
    host=host,
    password=passwd
)
cursor = conn.cursor()
#Creating the tables
try:
    cursor.execute(open('data/schema.sql', 'r').read())
except Exception as e:
    print(e)

# Inserting data in the database
data_path = 'data/datasetv1.csv'
with open(data_path, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row.
    for row in reader:
        print(row[0])
        name = row[1].replace("https://github.com/", "")
        folder_name = name.split("/")[-1]
        row.append(name)
        row.append(folder_name)
        cursor.execute(
            "INSERT INTO public.repos VALUES (%s, %s, %s, %s, %s)",
            row
        )
conn.commit()
cursor.close()
conn.close()


