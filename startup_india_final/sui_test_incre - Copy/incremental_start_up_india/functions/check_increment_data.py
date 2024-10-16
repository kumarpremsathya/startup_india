import re
import sys
import traceback
import pandas as pd
from config import startup_india_config
from functions import log, insert_excel_sheet_data_to_mysql, send_mail, yes_or_no ,removal

import pandas as pd
import traceback








def update_existing_rows_in_database(updated_rows_df):
    print("update_existing_rows_in_database function is called")
    connection = startup_india_config.db_connection()
    cursor = connection.cursor()
    try:
        count = 0
        for _, row in updated_rows_df.iterrows():
            # Handle NaN values by replacing them with None
            row = row.where(pd.notnull(row), None)
            pageurl = row.name  # Use the index (pageurl)
            
            # Check if the Updated_date is the current date
            check_query = f"""
                SELECT Updated_date FROM {startup_india_config.table_name}
                WHERE pageurl = %s
            """
            cursor.execute(check_query, (pageurl,))
            result = cursor.fetchone()
            
            # Proceed only if the Updated_date is not the current date
            if result and result[0] == startup_india_config.current_date:
                print(f"Skipping row with pageurl {pageurl} as it is already updated today")
                continue

            update_query = f"""
                UPDATE {startup_india_config.table_name}
                SET companyName= %s,
                    stage= %s,
                    focusIndustry= %s,
                    focusSector= %s,
                    serviceArea= %s,
                    location= %s,
                    companyURL= %s,
                    aboutDetails= %s,
                    joinedDate= %s,
                    activeSince= %s,
                    Updated_date = %s
                WHERE pageurl = %s
            """
            values = (
                row["companyName"],
                row["stage"],
                row["focusIndustry"],
                row["focusSector"],
                row["serviceArea"],
                row["location"],
                row["companyURL"],
                row["aboutDetails"],
                row["joinedDate"],
                row["activeSince"],
                startup_india_config.current_date,
                pageurl
            )
            cursor.execute(update_query, values)
            count += 1
        
        connection.commit()
        startup_india_config.updated_count = count
        print("Transaction committed successfully for updated rows")
    except Exception as e:
        print("Error updating rows:", e)
        traceback.print_exc()
        connection.rollback()
    finally:
        cursor.close()
        connection.close()




def check_increment_data(new_data_file):
    print("check increment data function is called")
    connection = startup_india_config.db_connection()
    cursor = connection.cursor()
    try:
        new_data = pd.read_excel(new_data_file, sheet_name='Sheet1')

        query = "SELECT * FROM sui_final"

        old_data = pd.read_sql(query, connection)

        # Get count of existing deleted sources
        existing_deleted_count_query = "SELECT COUNT(*) FROM sui_final WHERE company_availability_status = 'NO'"
        cursor.execute(existing_deleted_count_query)
        existing_deleted_count = cursor.fetchone()[0]


        unique_id = 'pageurl'

        new_data.set_index(unique_id, inplace=True)
        old_data.set_index(unique_id, inplace=True)
        ignore_columns = ['activeSince', 'joinedDate', 'aboutDetails', 'companyURL']

        def clean_text(text):
            if isinstance(text, str):
                return re.sub(r'[\s\-/:]', '', text)
            return text

        new_data_cleaned = new_data.applymap(clean_text)
        old_data_cleaned = old_data.applymap(clean_text)

        updated_count = 0
        new_data_count = 0
        deleted_count = 0

        update_info = []
        new_deleted_count = 0
        # deleted_pageurls = []
        new_deleted_pageurls = []

        sr_no = 1



      
        for index, row in new_data_cleaned.iterrows():
            if index in old_data_cleaned.index:
                changes = {}
                for col in new_data_cleaned.columns:
                    if col not in ignore_columns:
                        if not pd.isna(row[col]) and not pd.isna(old_data_cleaned.loc[index, col]) and row[col] != old_data_cleaned.loc[index, col]:
                            old_data.loc[index, col] = new_data.loc[index, col]  # Update with new data
                            changes[col] = new_data.loc[index, col]
                
                if changes:
                    old_data.loc[index, 'comments'] = 'Updated'
                    updated_count += 1
                    update_info.append({'pageurl': index, 'Changes': changes, 'Action': 'Updated'})
                    print(f"{sr_no}, Row with pageurl {index} compared: Changes detected and updated.")
                else:
                    print(f"{sr_no}, Row with pageurl {index} compared: No changes detected.")
            else:
                old_data.loc[index] = new_data.loc[index]
                old_data.loc[index, 'comments'] = 'newly inserted'
                new_data_count += 1
                update_info.append({'pageurl': index, 'Changes': new_data.loc[index].to_dict(), 'Action': 'Inserted'})
                print(f"{sr_no}, Row with pageurl {index} compared: New row inserted.")
            
            sr_no += 1

        # Check for newly deleted entries
        for index in old_data_cleaned.index:
            if index not in new_data_cleaned.index and old_data.loc[index, 'company_availability_status'] != 'NO':
                old_data.loc[index, 'comments'] = 'deleted_source'
                old_data.loc[index, 'company_availability_status'] = 'NO'
                new_deleted_count += 1
                new_deleted_pageurls.append({
                    'pageurl': index,
                    'companyName': old_data.loc[index, 'companyName']
                })
                print(f"{sr_no}, Row with pageurl {index} newly marked as deleted_source.")
                sr_no += 1
        
        print("new_deleted_count", new_deleted_count)
        print("new_deleted_pageurls", new_deleted_pageurls)

        updated_data = old_data[old_data['comments'].isin(['Updated', 'newly inserted', 'deleted_source'])]

        updated_rows = []
        for _, row in updated_data.iterrows():
            if row["comments"] == "Updated":
                updated_rows.append(row)

        if len(updated_rows) > 0:
            updated_rows_df = pd.DataFrame(updated_rows)
            print(updated_rows_df, "update_print")
            update_existing_rows_in_database(updated_rows_df)
        else:
            print(updated_rows, "there is no update")


        total_deleted_count = existing_deleted_count + new_deleted_count
        startup_india_config.total_deleted_count = total_deleted_count
        startup_india_config.new_deleted_sources = new_deleted_pageurls
        startup_india_config.new_deleted_count = new_deleted_count

        startup_india_config.newly_added = new_data_count
        
        # for row in deleted_pageurls:
        #     startup_india_config.deleted_sources += row + ", "

        increment_file_name = f"incremental_excel_sheet_{startup_india_config.current_date}.xlsx"
        increment_data_excel_path = fr"C:\Users\Premkumar.8265\Desktop\sui_test_incre - Copy\incremental_start_up_india\data\increment_data\{increment_file_name}"  

        updated_data.to_excel(increment_data_excel_path, index=True)
        print(f"Updated data saved to {increment_data_excel_path}")

        if len(new_deleted_pageurls) > 0:
            # yes_or_no.update_deleted_rows_in_database(r"C:\Users\Premkumar.8265\Desktop\sui_test_incre\incremental_start_up_india\data\excel_sheet\final_excels_2024-09-19.xlsx")
            
            removal.update_removal_dates()
            

        if deleted_count > 0 and new_data_count == 0:
            startup_india_config.log_list[1] = "Success"
            startup_india_config.log_list[3] = f"{startup_india_config.updated_count} data updated, {startup_india_config.deleted_source_count} data missing in the website"
            log.insert_log_into_table(startup_india_config.log_list)
            startup_india_config.log_list = [None] * 4
            sys.exit()

        elif new_data_count == 0:
            startup_india_config.log_list[1] = "Success"
            startup_india_config.log_list[3] = f"{startup_india_config.updated_count} data updated, no new data"
            log.insert_log_into_table(startup_india_config.log_list)
            startup_india_config.log_list = [None] * 4
            sys.exit()


        print(f"Number of rows updated: {startup_india_config.updated_count}")
        print(f"Number of new data inserted: {new_data_count}")


        print(f"Number of rows newly marked as deleted_source: {startup_india_config.new_deleted_count}")
        print(f"Total number of rows marked as deleted_source: {startup_india_config.total_deleted_count}")
        print("Newly Deleted pageURLs:", startup_india_config.new_deleted_sources)


        print("Update Information:")
        # for info in update_info:
        #     print(f"Action: {info['Action']}, pageurl: {info['pageurl']}, Changes: {info['Changes']}")
        insert_excel_sheet_data_to_mysql.insert_excel_data_to_mysql(increment_data_excel_path)

    except Exception as e:
        traceback.print_exc()
        startup_india_config.log_list[1] = "Failure"
        startup_india_config.log_list[2] = "error in checking part"
        log.insert_log_into_table(startup_india_config.log_list)
        send_mail.send_email("start up india source script error", str(e))
        startup_india_config.log_list = [None] * 4
        sys.exit()













# def update_existing_rows_in_database(updated_rows_df):
#     print("update_existing_rows_in_database function is called")
#     connection = startup_india_config.db_connection()
#     cursor = connection.cursor()
#     try:
#         count = 0
#         for _, row in updated_rows_df.iterrows():
#             # Handle NaN values by replacing them with None
#             row = row.where(pd.notnull(row), None)
#             pageurl = row.name  # Use the index (pageurl)
            
#             # Check if the Updated_date is the current date
#             check_query = f"""
#                 SELECT Updated_date FROM {startup_india_config.table_name}
#                 WHERE pageurl = %s
#             """
#             cursor.execute(check_query, (pageurl,))
#             result = cursor.fetchone()
            
#             # Proceed only if the Updated_date is not the current date
#             if result and result[0] == startup_india_config.current_date:
#                 print(f"Skipping row with pageurl {pageurl} as it is already updated today")
#                 continue

#             update_query = f"""
#                 UPDATE {startup_india_config.table_name}
#                 SET companyName= %s,
#                     stage= %s,
#                     focusIndustry= %s,
#                     focusSector= %s,
#                     serviceArea= %s,
#                     location= %s,
#                     companyURL= %s,
#                     aboutDetails= %s,
#                     joinedDate= %s,
#                     activeSince= %s,
#                     Updated_date = %s
#                 WHERE pageurl = %s
#             """
#             values = (
#                 row["companyName"],
#                 row["stage"],
#                 row["focusIndustry"],
#                 row["focusSector"],
#                 row["serviceArea"],
#                 row["location"],
#                 row["companyURL"],
#                 row["aboutDetails"],
#                 row["joinedDate"],
#                 row["activeSince"],
#                 startup_india_config.current_date,
#                 pageurl
#             )
#             cursor.execute(update_query, values)
#             count += 1
        
#         connection.commit()
#         startup_india_config.updated_count = count
#         print("Transaction committed successfully for updated rows")
#     except Exception as e:
#         print("Error updating rows:", e)
#         traceback.print_exc()
#         connection.rollback()
#     finally:
#         cursor.close()
#         connection.close()

# def check_increment_data(new_data_file):
#     print("check increment data function is called")
#     connection = startup_india_config.db_connection()
#     cursor = connection.cursor()
#     try:
#         new_data = pd.read_excel(new_data_file, sheet_name='Sheet1')

#         query = "SELECT * FROM sui_final"

#         old_data = pd.read_sql(query, connection)

#         unique_id = 'pageurl'

#         new_data.set_index(unique_id, inplace=True)
#         old_data.set_index(unique_id, inplace=True)
#         ignore_columns = ['activeSince', 'joinedDate', 'aboutDetails', 'companyURL']

#         def clean_text(text):
#             if isinstance(text, str):
#                 return re.sub(r'[\s\-/:]', '', text)
#             return text

#         new_data_cleaned = new_data.applymap(clean_text)
#         old_data_cleaned = old_data.applymap(clean_text)

#         updated_count = 0
#         new_data_count = 0
#         deleted_count = 0

#         update_info = []
#         deleted_pageurls = []

#         sr_no = 1

#         for index, row in new_data_cleaned.iterrows():
#             if index in old_data_cleaned.index:
#                 changes = {}
#                 for col in new_data_cleaned.columns:
#                     if col not in ignore_columns:
#                         if not pd.isna(row[col]) and not pd.isna(old_data_cleaned.loc[index, col]) and row[col] != old_data_cleaned.loc[index, col]:
#                             old_data.loc[index, col] = new_data.loc[index, col]  # Update with new data
#                             changes[col] = new_data.loc[index, col]
                
#                 if changes:
#                     old_data.loc[index, 'comments'] = 'Updated'
#                     updated_count += 1
#                     update_info.append({'pageurl': index, 'Changes': changes, 'Action': 'Updated'})
#                     print(f"{sr_no}, Row with pageurl {index} compared: Changes detected and updated.")
#                 else:
#                     print(f"{sr_no}, Row with pageurl {index} compared: No changes detected.")
#             else:
#                 old_data.loc[index] = new_data.loc[index]
#                 old_data.loc[index, 'comments'] = 'newly inserted'
#                 new_data_count += 1
#                 update_info.append({'pageurl': index, 'Changes': new_data.loc[index].to_dict(), 'Action': 'Inserted'})
#                 print(f"{sr_no}, Row with pageurl {index} compared: New row inserted.")
            
#             sr_no += 1

#         for index in old_data_cleaned.index:
#             if index not in new_data_cleaned.index:
#                 old_data.loc[index, 'comments'] = 'deleted_source'
#                 deleted_count += 1
#                 deleted_pageurls.append(index)
#                 print(f"{sr_no}, Row with pageurl {index} marked as deleted_source.")
#                 sr_no += 1

#         updated_data = old_data[old_data['comments'].isin(['Updated', 'newly inserted', 'deleted_source'])]

#         updated_rows = []
#         for _, row in updated_data.iterrows():
#             if row["comments"] == "Updated":
#                 updated_rows.append(row)

#         if len(updated_rows) > 0:
#             updated_rows_df = pd.DataFrame(updated_rows)
#             print(updated_rows_df, "update_print")
#             update_existing_rows_in_database(updated_rows_df)
#         else:
#             print(updated_rows, "there is no update")



#         startup_india_config.deleted_source_count = deleted_count
        
#         # for row in deleted_pageurls:
#         #     startup_india_config.deleted_sources += row + ", "

#         increment_file_name = f"incremental_excel_sheet_{startup_india_config.current_date}.xlsx"
#         increment_data_excel_path = fr"C:\Users\Premkumar.8265\Desktop\sui_test_incre\incremental_start_up_india\data\increment_data\{increment_file_name}"  

#         updated_data.to_excel(increment_data_excel_path, index=True)
#         print(f"Updated data saved to {increment_data_excel_path}")

#         if len(deleted_pageurls) > 0:
#             yes_or_no.update_deleted_rows_in_database(r"C:\Users\Premkumar.8265\Desktop\sui_test_incre\incremental_start_up_india\data\excel_sheet\final_excels_2024-09-19.xlsx")
            
#             removal.update_removal_dates()
            

#         if deleted_count > 0 and new_data_count == 0:
#             startup_india_config.log_list[1] = "Success"
#             startup_india_config.log_list[3] = f"{startup_india_config.updated_count} data updated, {startup_india_config.deleted_source_count} data missing in the website"
#             log.insert_log_into_table(startup_india_config.log_list)
#             startup_india_config.log_list = [None] * 4
#             sys.exit()

#         elif new_data_count == 0:
#             startup_india_config.log_list[1] = "Success"
#             startup_india_config.log_list[3] = f"{startup_india_config.updated_count} data updated, no new data"
#             log.insert_log_into_table(startup_india_config.log_list)
#             startup_india_config.log_list = [None] * 4
#             sys.exit()


#         print(f"Number of rows updated: {startup_india_config.updated_count}")
#         print(f"Number of new data inserted: {new_data_count}")
#         print(f"Number of rows marked as deleted_source: {startup_india_config.deleted_source_count}")
#         print("Update Information:")
#         # for info in update_info:
#         #     print(f"Action: {info['Action']}, pageurl: {info['pageurl']}, Changes: {info['Changes']}")
#         # insert_excel_sheet_data_to_mysql.insert_excel_data_to_mysql(increment_data_excel_path)

#     except Exception as e:
#         traceback.print_exc()
#         startup_india_config.log_list[1] = "Failure"
#         startup_india_config.log_list[2] = "error in checking part"
#         log.insert_log_into_table(startup_india_config.log_list)
#         send_mail.send_email("start up india source script error", str(e))
#         startup_india_config.log_list = [None] * 4
#         sys.exit()
