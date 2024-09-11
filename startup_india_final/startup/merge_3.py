import pandas as pd

# File paths
file1_path = r'C:\Users\Premkumar.8265\Desktop\startup\API_combined_09_09_2024.xlsx'
file2_path = r'C:\Users\Premkumar.8265\Desktop\startup\db_data_09_09_2024.xlsx'

# Load Excel files into DataFrames
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

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
merged_file_path = 'merged_output_09_09_2024.xlsx'
merged_df.to_excel(merged_file_path, index=False)

# Filter rows where 'companyName' is empty
empty_company_name_df = merged_df[merged_df['companyName'].isna()]

# Extract 'pageurl' values where 'companyName' is empty
empty_pageurls_df = empty_company_name_df[['pageurl', 'API_urls']]

# Save these pageurl values to a new Excel file
empty_pageurls_file_path = 'incremental_pageurls_09_09_2024.xlsx'
empty_pageurls_df.to_excel(empty_pageurls_file_path, index=False)

print(f'Merged data saved to {merged_file_path}')
print(f'Pageurls with empty companyName saved to {empty_pageurls_file_path}')



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

