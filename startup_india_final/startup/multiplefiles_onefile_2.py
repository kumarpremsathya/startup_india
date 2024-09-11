import os
import pandas as pd

# Folder containing Excel files
folder_path = r"C:\Users\Premkumar.8265\Desktop\sui\test_09_09_24"

# Function to read all Excel files in a folder
def read_excel_files(folder_path):
    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_excel(file_path)
            all_data.append(df)
    return all_data

# Concatenate all dataframes into a single dataframe
def concatenate_dataframes(dataframes):
    if len(dataframes) == 0:
        return None
    combined_df = pd.concat(dataframes, ignore_index=True)
    # Remove duplicate rows if needed
    combined_df = combined_df.drop_duplicates()
    return combined_df

# Read all Excel files
excel_data = read_excel_files(folder_path)

# Concatenate dataframes
combined_data = concatenate_dataframes(excel_data)

if combined_data is not None:
    # Save the combined data to a single Excel file
    combined_file_path = "API_7th_sui.xlsx"
    combined_data.to_excel(combined_file_path, index=False)

    print("Combined data saved to:", combined_file_path)
else:
    print("No data to concatenate.")
