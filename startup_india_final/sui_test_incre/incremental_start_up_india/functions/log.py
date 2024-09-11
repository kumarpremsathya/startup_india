from config import startup_india_config
from functions import get_data_count_database

def insert_log_into_table(log_list):
    print("insert_log_into_table function is called")
    connection = startup_india_config.db_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO startup_india_log (source_name, script_status, data_available, data_scraped, total_record_count, failure_reason, comments, deleted_source, deleted_source_count, source_status)
        VALUES (%(source_name)s, %(script_status)s, %(data_available)s, %(data_scraped)s, %(total_record_count)s, %(failure_reason)s, %(comments)s, %(deleted_source)s, %(deleted_source_count)s, %(source_status)s)
    """
    values = {
        'source_name': startup_india_config.source_name,
        'script_status': log_list[1] if log_list[1] else None,
        'data_available': startup_india_config.no_data_avaliable if startup_india_config.no_data_avaliable else None  ,
        'data_scraped': startup_india_config.no_data_scraped if startup_india_config.no_data_scraped else None,
        'total_record_count': get_data_count_database.get_data_count_database(),
        'failure_reason': log_list[2] if log_list[2] else None,
        'comments': log_list[3] if log_list[3] else None,
        'deleted_source': startup_india_config.deleted_sources if startup_india_config.deleted_sources else None,
        'deleted_source_count': startup_india_config.deleted_source_count,
        'source_status': startup_india_config.source_status

    }

    cursor.execute(query, values)
    print("log list", values)
    connection.commit()
    connection.close()
