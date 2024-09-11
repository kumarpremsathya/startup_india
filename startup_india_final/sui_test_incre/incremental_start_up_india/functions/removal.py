import pandas as pd
from datetime import datetime

# Assuming startup_india_config provides a function for database connection
from config import startup_india_config

def update_removal_dates():
    print("update removal dates function is called")
    # Load the Excel files
    last_month_df = pd.read_excel(r'C:\Users\Premkumar.8265\Desktop\sui_test_incre\incremental_start_up_india\data\increment_data\incremental_excel_sheet_2024-09-10.xlsx')
    current_month_df = pd.read_excel(r'C:\Users\Premkumar.8265\Desktop\sui_test_incre\incremental_start_up_india\data\increment_data\incremental_excel_sheet_2024-09-03.xlsx')

    # Filter last month's data where 'comments' are 'deleted source'
    deleted_source_last_month = last_month_df[last_month_df['comments'].str.contains('deleted_source', na=False)]

    # Compare 'pageurl' of last month's deleted sources with current month's 'pageurl'
    # to identify URLs that no longer exist in the current month's data
    removed_urls = deleted_source_last_month[~deleted_source_last_month['pageurl'].isin(current_month_df['pageurl'])]

    # Use the existing database connection from startup_india_config
    connection = startup_india_config.db_connection()
    cursor = connection.cursor()

    try:
        # Iterate through the removed URLs and update the 'removal_date' in the database
        for index, row in removed_urls.iterrows():
            removal_date = datetime.now().strftime('%Y-%m-%d')
            query = f"UPDATE {startup_india_config.table_name} SET removal_date = %s WHERE pageurl = %s"
            cursor.execute(query, (removal_date, row['pageurl']))

        # Commit the transaction
        connection.commit()

        print("Comparison complete. The 'removal_date' has been updated in the database for the removed URLs.")
    
    except Exception as e:
        print("Error updating removal dates in the database:", e)
        connection.rollback()
    
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()



