# import pandas as pd
# import re

# # Load the Excel file
# file_path = r'C:\Users\Premkumar.8265\Desktop\sui\missing_dipp.xlsx'
# df = pd.read_excel(file_path)

# # Function to extract the ID from the URL
# def extract_id(url):
#     if isinstance(url, str):  # Ensure url is a string
#         match = re.search(r'profile\.Startup\.([a-f0-9]{24})\.html', url)
#         if match:
#             return match.group(1)
#     return None

# # Convert 'pageurl' column to string to avoid errors
# df['pageurl'] = df['pageurl'].astype(str)

# # Apply the function to extract IDs
# df['ID'] = df['pageurl'].apply(extract_id)

# # Save the updated DataFrame to a new Excel file
# output_file_path = 'updated_excel_file.xlsx'
# df.to_excel(output_file_path, index=False)

# print(f'IDs extracted and saved to {output_file_path}')


import pandas as pd

# Define the base URL
base_url = 'https://api.startupindia.gov.in/sih/api/common/replica/user/profile/'

# Read the Excel file
input_file = r'C:\Users\Premkumar.8265\Desktop\sui\updated_excel_file.xlsx'
df = pd.read_excel(input_file)

# Ensure the column name is correct
if 'ID' not in df.columns:
    raise ValueError("Column 'ID' not found in the input file.")

# Generate the URLs
df['URL'] = base_url + df['ID'].astype(str)

# Save the results to a new Excel file
output_file = 'excel_file_api_old.xlsx'
df[['URL']].to_excel(output_file, index=False)

print(f"URLs have been written to {output_file}")