import sys
import traceback
import pandas as pd
from config import startup_india_config
from functions import send_mail, log


def insert_excel_data_to_mysql(final_excel_sheets_path):
    print("insert_excel_data_to_mysql function is called")
    connection = startup_india_config.db_connection()
    cursor = connection.cursor()
    try:
        df = pd.read_excel(final_excel_sheets_path)
        df = df.where(pd.notnull(df), None)
        data_inserted = 0
        for index, row in df.iterrows():
            if row["comments"] == "newly inserted":
                check_query = "SELECT COUNT(*) FROM sui_final WHERE pageurl = %s"
                cursor.execute(check_query, (row["pageurl"],))  # Added comma to make it a tuple
                count = cursor.fetchone()[0]
                if count == 0:
                    insert_query = f"""
                        INSERT INTO {startup_india_config.table_name} (DPIIT, companyName, stage, focusIndustry, focusSector, serviceArea,
                                                location, noOfYear, companyURL, aboutDetails,joinedDate, DPIITRecognised,activeSince,dipp_number,legalName,cin,pan,pageurl,company_availability_status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                    values = (
                        row['DPIIT'],
                        row['companyName'],
                        row['stage'],
                        row['focusIndustry'],
                        row['focusSector'],
                        row['serviceArea'],
                        row['location'],
                        row['noOfYear'],
                        row['companyURL'],
                        row['aboutDetails'],
                        row['joinedDate'],
                        row['DPIITRecognised'],
                        row['activeSince'],
                        row['dipp_number'],
                        row['legalName'],
                        row['cin'],
                        row['pan'],
                        row['pageurl'],
                        'YES'  # Set company_availability_status to 'YES' for new entries
                        
                    )

                    # Replace None and NaN values with NULL
                    values = tuple(None if pd.isna(v) else v for v in values)
                    
                    # print(f"Inserting row {index}: {values}")  # Debugging line
                    cursor.execute(insert_query, values)
                    data_inserted += 1
        connection.commit()
        startup_india_config.no_data_avaliable = data_inserted+startup_india_config.updated_count
        startup_india_config.no_data_scraped = data_inserted+startup_india_config.updated_count
        print("Data inserted into the database table")
        startup_india_config.log_list[1] = "Success"
        startup_india_config.log_list[3] = f"{startup_india_config.updated_count} data updated, {startup_india_config.newly_added} new data, {startup_india_config.new_deleted_count} newly deleted "
        log.insert_log_into_table(startup_india_config.log_list)
        startup_india_config.log_list = [None] * 4

    except Exception as e:
        startup_india_config.log_list[1] = "Failure"
        startup_india_config.log_list[2] = "error in insert part"
        log.insert_log_into_table(startup_india_config.log_list)
        startup_india_config.log_list = [None] * 4
        traceback.print_exc()
        send_mail.send_email("start up india script error", str(e))
        sys.exit("script error")
