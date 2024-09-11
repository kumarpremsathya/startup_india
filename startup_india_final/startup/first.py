import pandas as pd
from sqlalchemy import create_engine

# File path to your Excel file
excel_file_path = r'C:\Users\Premkumar.8265\Desktop\startup\db_data_09_09_2024.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

# MySQL database connection details
DATABASE_TYPE = 'mysql'
DBAPI = 'pymysql'
HOST = 'localhost'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'startup'
PORT = 3306

# Create a connection string
connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Create a SQLAlchemy engine
engine = create_engine(connection_string)

# Store the DataFrame in the MySQL table 'sui_final'
df.to_sql('sui_final', engine, if_exists='replace', index=False)

print("DataFrame has been stored in the MySQL database.")
