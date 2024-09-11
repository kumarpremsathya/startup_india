# import pandas as pd
# import requests
# import time
# import os

# # Define the API endpoint and headers
# url = "https://api.startupindia.gov.in/sih/api/noauth/search/profiles"


# headers = {
#     'Content-Type': 'application/json',
#     'User-Agent': 'PostmanRuntime/7.35.0',
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Connection': 'keep-alive'
# }

# # Template for the payload
# payload_template = {
#     "query": "",
#     "focusSector": False,
#     "industries": [],
#     "sectors": [],
#     "states": [],
#     "legalName":[],
#     "badges": [],
#     "city": [],
#     "dippNumber":[],
#     "dippRecognitionStatus":[],
#     "services":[],
#     "dpiitRecogniseUser": False,
#     "internationalUser": False,
#     "page": 0,  # Placeholder for page number
#     "roles": ["Startup"],
#     "sort": {
#         "orders": [
#             {
#                 "field": "registeredOn",
#                 "direction": "DESC"
#             }
#         ]
#     },
#     "stages": []
# }
# def save_data_to_excel(data, file_name):
#     # Convert the data to a DataFrame
#     df = pd.DataFrame(data, columns=[ "id","name","dippNumber","dippRecognitionStatus","state","industries","sectors"])

#     # Add page URL
#     df["page_url"] = df["id"].apply(lambda x: f"https://www.startupindia.gov.in/content/sih/en/profile.Startup.{x}.html")

#     # df = df.drop(columns=['id'])

#     # Check if the file already exists
#     if os.path.exists(file_name):
#         # Append data to the existing file
#         existing_df = pd.read_excel(file_name)
#         combined_df = pd.concat([existing_df, df])
#         combined_df.to_excel(file_name, index=False)
#     else:
#         # Create a new file with the data
#         df.to_excel(file_name, index=False)
#         print(f"Data saved to {file_name}")

# def fetch_all_data_for_state(state_id, state_name):
#     all_data = []
    
#     page_num = 0
#     folder_name = 'test'
#     os.makedirs(folder_name, exist_ok=True)  # Create the folder if it doesn't exist
#     file_name = os.path.join(folder_name, f"{state_name}.xlsx")
    
#     while True:
#         payload = payload_template.copy()
#         payload["states"] = [state_id]
#         payload["page"] = page_num
#         response = requests.post(url, headers=headers, json=payload)
#         if response.status_code == 200:
#             data = response.json().get("content", [])
#             if not data:
#                 break  # Exit the loop if no more data is returned
#             all_data.extend(data)
#             print(f"Fetched page {page_num} for s                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      tate: {state_name}")
#             save_data_to_excel(data, file_name)  # Save data for the current page
#             page_num += 1
#             time.sleep(2)
#         else:
#             print(f"Request failed with status code: {response.status_code} for state: {state_name} on page: {page_num}")
#             break
    
#     if not all_data:
#         print(f"No data found for state: {state_name}")

# # Read state IDs from the provided Excel sheet
# state_data = pd.read_excel(r"C:\Users\Premkumar.8265\Desktop\sui\state_id.xlsx")

# # Iterate through each state ID and fetch data
# for index, row in state_data.iterrows():
#     state_name = row['state']
#     state_id = row['state_id']
#     fetch_all_data_for_state(state_id, state_name)  

# print("Data fetching and saving completed.")










import requests
import pandas as pd
import time

# Define the input and output file paths
input_file = r'C:\Users\Premkumar.8265\Desktop\sui\excel_file_api_old.xlsx'
output_file = 'SUI_pen.xlsx'

# Define the base URL template

# Read the URLs from the Excel file
df_urls = pd.read_excel(input_file, sheet_name='Sheet1')  # Adjust sheet_name if needed
urls = df_urls['URL']

# Prepare a DataFrame to store all the results
results = []

# Define headers for the requests
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'PostmanRuntime/7.35.0',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

# Iterate over each URL
for url in urls:
    try:
        # Send a GET request to the API
        response = requests.get(url, headers=headers)
        time.sleep(3)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Extract the required fields with default values if missing
        user = data.get('user', {})
        startup = user.get('startup', {})
        legalName = startup.get('legalName', 'N/A')
        cin = startup.get('cin', 'N/A')
        pan = startup.get('pan', 'N/A')



        # Append the extracted data to the results list
        results.append({
            
            'legalName': legalName,
            'cin':cin,
            'pan':pan,
  # Add the page URL to the results
        })
        time.sleep(3) 
        # Save to Excel after each request
        df_results = pd.DataFrame(results)
        df_results.to_excel(output_file, index=False, engine='openpyxl')
        
        # Wait for 3 seconds before the next request
       

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

print(f"Data has been saved to {output_file}")


