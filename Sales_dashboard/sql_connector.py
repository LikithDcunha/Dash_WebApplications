import csv
import mysql.connector   ## pip install --upgrade mysql-connector-python (if connections SHa2 auth error)
import pandas as pd
import yaml



#--- Loading credentials 

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

cursor.execute('Show Tables;')
print(cursor.fetchall())

tables = ['customers', 'date', 'markets', 'products', 'transactions']


dfs = {}

for table in tables:
    cursor.execute(f'SELECT * FROM {table}')
    temp_result = cursor.fetchall()
    df = pd.DataFrame(temp_result, columns=[col[0] for col in cursor.description])
    # storing the df in the dictionary with dataframe as value, table name as key
    dfs[table] = df


def transform_data_tocsv(dfs, output_folder='./'):
    for table_name, table_data in dfs.items():
        csv_file_path = f"{output_folder}/{table_name}.csv"
        table_data.to_csv(csv_file_path,index=False)
        print(f'table {table_name} written to {csv_file_path}')

transform_data_tocsv(dfs,output_folder='Sales_dashboard/sales_extracted_data')


def transform_data_tocsv(tables_dict, output_folder='./'):
    for table_name, table_data in tables_dict.items():
        csv_file_path = f"{output_folder}/{table_name}.csv"
        table_data.to_csv(csv_file_path, index=False)
        print(f'Table {table_name} written to {csv_file_path}')



# for result in cursor.fetchall():
#     print(result)



# Input queries for DA

# query = ''
# try:
#     cursor.execute(query)
#     results = cursor.fetchall()
#     df = pd.DataFrame(results, columns=[column[0] for column in cursor.description])
#     print(df)
# except mysql.connector.Error as err:
#     # Handle Errors
#     print("Error: {}".format(err))


# Close 
cursor.close()
cnx.close()



