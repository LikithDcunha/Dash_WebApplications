import csv
import mysql.connector   ## pip install --upgrade mysql-connector-python (if connections SHa2 auth error)
import pandas as pd
import yaml



with open("build/creds.yml") as f:
    cred_content = f.read()

my_creds = yaml.load(cred_content, Loader= yaml.FullLoader)

host,user,password,database = my_creds["host"],my_creds["user"],my_creds["password"],my_creds["database"]


# Connect to MySQL
cnx = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor = cnx.cursor()

#Testing connection with a query
query = """ 
            SELECT *
            from customers
            Order by 1;

        """

cursor.execute(query)
temp_result = cursor.fetchall()
df = pd.DataFrame(temp_result, columns=[row[0] for row in cursor.description])
print(df.head(10))

for result in cursor.fetchall():
    print(result)




# Input queries for DA

try:
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=[column[0] for column in cursor.description])
    print(df)
except mysql.connector.Error as err:
    # Handle Errors
    print("Error: {}".format(err))


# Close 
cursor.close()
cnx.close()



