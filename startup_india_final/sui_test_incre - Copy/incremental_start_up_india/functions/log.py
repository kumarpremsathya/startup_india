from config import startup_india_config
from functions import get_data_count_database,send_mail,log
import sys
import traceback
import json
from datetime import datetime

def insert_log_into_table(log_list):
    print("insert_log_into_table function is called")
    

    try:
        removal_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connection = startup_india_config.db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO startup_india_log (source_name, script_status, data_available, data_scraped, total_record_count, failure_reason, comments, newly_added_count, updated_source_count, deleted_source, deleted_source_count, source_status, removal_date)
            VALUES (%(source_name)s, %(script_status)s, %(data_available)s, %(data_scraped)s, %(total_record_count)s, %(failure_reason)s, %(comments)s, %(newly_added_count)s, %(updated_source_count)s, %(deleted_source)s, %(deleted_source_count)s, %(source_status)s, %(removal_date)s)
        """
        values = {
            'source_name': startup_india_config.source_name,
            'script_status': log_list[1] if log_list[1] else None,
            'data_available': startup_india_config.no_data_avaliable if startup_india_config.no_data_avaliable else None  ,
            'data_scraped': startup_india_config.no_data_scraped if startup_india_config.no_data_scraped else None,
            'total_record_count': get_data_count_database.get_data_count_database(),
            'failure_reason': log_list[2] if log_list[2] else None,
            'comments': log_list[3] if log_list[3] else None,
            'newly_added_count':startup_india_config.newly_added if startup_india_config.newly_added else None,
            'updated_source_count':startup_india_config.updated_count if startup_india_config.updated_count else None,
            
            'deleted_source': json.dumps(startup_india_config.new_deleted_sources) if startup_india_config.new_deleted_sources else None,
            'deleted_source_count': startup_india_config.new_deleted_count,
            'source_status': startup_india_config.source_status,
            'removal_date':removal_date if startup_india_config.new_deleted_count else None,

        }

        cursor.execute(query, values)
        print("log list", values)
        connection.commit()
        connection.close()
    except Exception as e:
        traceback.print_exc()
        startup_india_config.log_list[1] = "Failure"
        startup_india_config.log_list[2] = "error in inserting log table"
        log.insert_log_into_table(startup_india_config.log_list)
        send_mail.send_email("start up india source script error", str(e))
        startup_india_config.log_list = [None] * 4
        sys.exit()
