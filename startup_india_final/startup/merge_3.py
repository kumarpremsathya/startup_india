import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime



# MySQL connection details
db_username = 'root1'
db_password = 'Mysql1234$'
db_host = '4.213.77.165'
db_name = 'startup_india'
table_name = 'sui_final'


current_date = datetime.now().strftime("%Y-%m-%d")
combined_file_name = f"api_results_combined_{current_date}.xlsx"
combined_file1_path  = fr"C:\Users\Premkumar.8265\Desktop\startup\data\api_results_combined\{combined_file_name}"
  

# File path for the first Excel file
# file1_path = r'C:\Users\Premkumar.8265\Desktop\startup\API_combined_09_09_2024.xlsx'

# Create a connection string for MySQL
connection_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}"

# Create a database engine
engine = create_engine(connection_string)

# Load the Excel file into a DataFrame (df1)
df1 = pd.read_excel(combined_file1_path)

# Load the MySQL table into a DataFrame (df2)
df2 = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)

# # File paths
# file1_path = r'C:\Users\Premkumar.8265\Desktop\startup\API_combined_09_09_2024.xlsx'
# file2_path = r'C:\Users\Premkumar.8265\Desktop\startup\db_data_09_09_2024.xlsx'

# # Load Excel files into DataFrames
# df1 = pd.read_excel(file1_path)
# df2 = pd.read_excel(file2_path)

# Columns to merge from df1 (excluding columns that will duplicate in df2)
columns_to_merge = ['id', 'API_urls']

# Merge DataFrames on 'pageurl'
merged_df = pd.merge(df1[columns_to_merge + ['pageurl']], df2, on='pageurl', how='left')


# Desired column order
desired_columns = [
    'DPIIT', 'companyName', 'stage', 'focusIndustry', 'focusSector', 'serviceArea',
    'location', 'noOfYear', 'companyURL', 'aboutDetails', 'joinedDate',
    'DPIITRecognised', 'activeSince', 'pageurl','API_urls', 'Updated_date', 'dipp_number',
    'legalName', 'cin', 'pan', 'company_availability_status', 'dateofScrapping'
]

# Reorder columns
merged_df = merged_df[desired_columns]

# Save merged data to a new Excel file

current_date = datetime.now().strftime("%Y-%m-%d")
merged_file_name = f"merged_output_{current_date}.xlsx"
merged_file_path = fr"C:\Users\Premkumar.8265\Desktop\startup\data\merged_output\{merged_file_name}"


# merged_file_path = 'merged_output_09_09_2024.xlsx'
merged_df.to_excel(merged_file_path, index=False)

# Filter rows where 'companyName' is empty
empty_company_name_df = merged_df[merged_df['companyName'].isna()]

# Extract 'pageurl' values where 'companyName' is empty
empty_pageurls_df = empty_company_name_df[['pageurl', 'API_urls']]

# Save these pageurl values to a new Excel file
current_date = datetime.now().strftime("%Y-%m-%d")
incremental_pageurls_file_name = f"incremental_pageurls_{current_date}.xlsx"
incremental_pageurls_file_path = fr"C:\Users\Premkumar.8265\Desktop\startup\data\incremental_pageurls\{incremental_pageurls_file_name}"



# empty_pageurls_file_path = 'incremental_pageurls_09_09_2024.xlsx'
empty_pageurls_df.to_excel(incremental_pageurls_file_path, index=False)

print(f'Merged data saved to {merged_file_path}')
print(f'Pageurls with empty companyName saved to {incremental_pageurls_file_path}')



# import pandas as pd

# # File paths
# file1_path = r'C:\Users\Premkumar.8265\Desktop\startup\API_combined_1.xlsx'
   
# file2_path = r'C:\Users\Premkumar.8265\Desktop\startup\db_data_1.xlsx'  # Update with your actual file path

# # Load Excel files into DataFrames
# df1 = pd.read_excel(file1_path)
# df2 = pd.read_excel(file2_path)

# # Columns to merge
# merge_columns = [
#     'DPIIT','companyName', 'stage', 'focusIndustry', 'focusSector',
#     'serviceArea', 'location', 'noOfYear', 'companyURL', 'aboutDetails',
#     'joinedDate', 'DPIITRecognised', 'activeSince', 'pageurl', 'Updated_date','dipp_number','legalName','cin','pan','company_availability_status',
#     'dateofScrapping'
# ]

# # Merge DataFrames on 'pageurl'
# merged_df = pd.merge(df1, df2, on='pageurl', how='left')
# # merged_df = pd.merge(df2, df1[merge_columns], on='pageurl', how='left', suffixes=('_file_1', '_Book2'))

# # Identify ignored pageurls (not found in df1)


# # Save merged data to a new Excel file
# merged_file_path = 'merged_output_2.xlsx'
# merged_df.to_excel(merged_file_path, index=False)

# # Save ignored pageurls to another Excel file


# print(f'Merged data saved to {merged_file_path}')

