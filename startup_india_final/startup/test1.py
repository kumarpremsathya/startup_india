# import pandas as pd

# def find_deleted_pageurls(last_week_file, this_week_file):
#     # Read the Excel files
#     df_last_week = pd.read_excel(last_week_file)
#     df_this_week = pd.read_excel(this_week_file)

#     # Get the set of pageurls from both weeks
#     last_week_pageurls = set(df_last_week['pageurl'])
#     this_week_pageurls = set(df_this_week['pageurl'])

#     # Find the deleted pageurls
#     deleted_pageurls = last_week_pageurls - this_week_pageurls

#     return deleted_pageurls

# def main():
#     last_week_file = r"C:\Users\Premkumar.8265\Desktop\startup\data\final_excels\final_excels.xlsx"
#     this_week_file = r"C:\Users\Premkumar.8265\Desktop\startup\data\final_excels\final_excels_09_09_2024.xlsx"

#     deleted_pageurls = find_deleted_pageurls(last_week_file, this_week_file)

#     print(f"Number of deleted pageurls: {len(deleted_pageurls)}")
#     print("\nDeleted pageurls:")
#     for url in deleted_pageurls:
#         print(url)

#     # Optionally, save the deleted pageurls to a file
#     with open('deleted_pageurls.txt', 'w') as f:
#         for url in deleted_pageurls:
#             f.write(f"{url}\n")

#     print("\nDeleted pageurls have been saved to 'deleted_pageurls.txt'")

# if __name__ == "__main__":
#     main()






import pandas as pd

# Load last week's and this week's Excel files
last_week_file =  r"C:\Users\Premkumar.8265\Desktop\startup\data\final_excels\final_excels_2024-09-19.xlsx"


this_week_file = r"C:\Users\Premkumar.8265\Desktop\startup\data\final_excels\final_excels_2024-09-27.xlsx"


# Read the Excel files into dataframes
df_last_week = pd.read_excel(last_week_file)
df_this_week = pd.read_excel(this_week_file)

# Extract the 'pageurl' column from both dataframes
last_week_urls = set(df_last_week['pageurl'].dropna())
this_week_urls = set(df_this_week['pageurl'].dropna())

# Find URLs that were in last week's data but not in this week's data
deleted_urls = last_week_urls - this_week_urls

# Convert the result to a DataFrame for easier handling
df_deleted_urls = df_last_week[df_last_week['pageurl'].isin(deleted_urls)]

# Save the deleted URLs to a new Excel file
output_file = 'deleted_pageurls3.xlsx'
df_deleted_urls.to_excel(output_file, index=False)

print(f"Deleted page URLs have been saved to {output_file}")



