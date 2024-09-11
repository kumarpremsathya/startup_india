import mysql.connector
import pandas as pd


def convert_to_dict_from_excel(file_path, column_name1, column_name2):
    df = pd.read_excel(file_path)
    dic = df.set_index(column_name1)[column_name2].to_dict()
    return dic





def database_connection(localhost, db_username, db_password, database_name):
    """
    Example of object creation ->

    mydb = data_provider.database_connection("localhost", "root", "12345", "pandas")

    :param localhost: localhost or enter the host ip
    :param db_username: your db name
    :param db_password: your db master password
    :param database_name: your db name
    :return: database object
    """
    mydb = mysql.connector.connect(
        host=localhost,
        user=db_username,
        password=db_password,
        database=database_name
    )

    return mydb


def execute_query(mydb, query):
    cursor = mydb.cursor()
    cursor.execute(query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

def commit_to_db(mydb):
    mydb.commit()



def database_to_df(dbConnection, table_name):
    df = pd.read_sql(table_name, con=dbConnection)
    return df


def sql_table_to_db(dbConnection, df, table_name):
    df.to_sql(table_name, con=dbConnection, if_exists='append', index=False)
    print("Data is written in the database")




















    # def rename_columns(file_path, dic_file_path, column_name1, column_name2):
#     df = pd.read_excel(file_path)
#     df.rename(columns=convert_to_dict_from_excel(dic_file_path, column_name1, column_name2),
#               inplace=True)
#     return df




