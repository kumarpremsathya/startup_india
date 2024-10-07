import sys
import traceback
import pandas as pd 
from config import startup_india_config
from functions import log, send_mail

def update_deleted_rows_in_database(excel_file):
    print("update_deleted_rows_in_database function is called")
    connection = startup_india_config.db_connection()
    cursor = connection.cursor()
    try:
        
        if connection.is_connected():
            cursor = connection.cursor()

            df = pd.read_excel(excel_file)

            # Get all pageurls from Excel
            excel_pageurls = set(df['pageurl'].tolist())

            # Fetch all pageurls from database
            cursor.execute("SELECT pageurl FROM sui_final")
            db_pageurls = set(row[0] for row in cursor.fetchall())

            # Determine pageurls to update
            yes_pageurls = excel_pageurls.intersection(db_pageurls)
            no_pageurls = db_pageurls - excel_pageurls

            # Batch update for "YES" company_availability_status
            if yes_pageurls:
                yes_query = "UPDATE sui_final SET company_availability_status = 'YES' WHERE pageurl IN (%s)" % ','.join(['%s'] * len(yes_pageurls))
                cursor.execute(yes_query, tuple(yes_pageurls))

            # Batch update for "NO" company_availability_status
            if no_pageurls:
                no_query = "UPDATE sui_final SET company_availability_status = 'NO' WHERE pageurl IN (%s)" % ','.join(['%s'] * len(no_pageurls))
                cursor.execute(no_query, tuple(no_pageurls))

            # Commit changes
            connection.commit()
            print(f"Database updated successfully. YES: {len(yes_pageurls)}, NO: {len(no_pageurls)}")

    except Exception as e:
        traceback.print_exc()
        startup_india_config.log_list[1] = "Failure"
        startup_india_config.log_list[2] = "error in yes or no part"
        log.insert_log_into_table(startup_india_config.log_list)
        send_mail.send_email("start up india source script error", str(e))
        startup_india_config.log_list = [None] * 4
        sys.exit()
