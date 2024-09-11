import pandas as pd

pre_final_df = pd.read_excel(r"C:\Users\Premkumar.8265\Desktop\startup\merged_output_2.xlsx")

merged_df = pd.read_excel(r"C:\Users\Premkumar.8265\Desktop\startup\combined_page_apiurls.xlsx")

final_df = pd.merge(pre_final_df, merged_df, on='pageurl', how='left')


# Fill missing values in 'x' columns with corresponding 'y' columns
for col in final_df.columns:
    if col.endswith('_x'):
        base_col = col[:-2]  # Remove '_x' suffix to get the base column name
        y_col = base_col + '_y'
        if y_col in final_df.columns:
            final_df[base_col] = final_df[col].combine_first(final_df[y_col])

# Drop the '_x' and '_y' columns after merging
final_df = final_df[[col for col in final_df.columns if not col.endswith('_x') and not col.endswith('_y')]]




# # Desired column order
desired_columns = [
    'DPIIT', 'companyName', 'stage', 'focusIndustry', 'focusSector', 'serviceArea',
    'location', 'noOfYear', 'companyURL', 'aboutDetails', 'joinedDate',
    'DPIITRecognised', 'activeSince', 'pageurl', 'Updated_date', 'dipp_number',
    'legalName', 'cin', 'pan', 'company_availability_status', 'dateofScrapping'
]


# Reorder columns
final_df = final_df[desired_columns]


# Remove rows where 'companyName' column has empty values
final_df = final_df.dropna(subset=['companyName'])

final_file_path = 'final_excels.xlsx'
final_df.to_excel(final_file_path, index=False)


print(f"Data has been saved to {final_file_path}")

