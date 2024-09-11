from config import startup_india_config


def get_data_count_database():
    connection = startup_india_config.db_connection()
    cursor = connection.cursor()
    try:
        query = f"SELECT COUNT(*) FROM {startup_india_config.table_name}"
        cursor.execute(query)
        result = cursor.fetchone()
        print("Result from database query:", result)
        if result:
            return result[0]
        else:
            raise ValueError("Query did not return any results")
    except Exception as e:
        print("Error fetching data count from database:", e)
        raise
