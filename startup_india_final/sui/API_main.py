import pandas as pd
import requests
import time
import os

# Define the API endpoint and headers
url = "https://api.startupindia.gov.in/sih/api/noauth/search/profiles"


headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'PostmanRuntime/7.35.0',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

# Template for the payload
payload_template = {
    "query": "",
    "focusSector": False,
    "industries": [],
    "sectors": [],
    "states": [],
    "legalName":[],
    "badges": [],
    "city": [],
    "dippNumber":[],
    "dippRecognitionStatus":[],
    "services":[],
    "dpiitRecogniseUser": True,
    "internationalUser": False,
    "page": 0,  # Placeholder for page number
    "roles": ["Startup"],
    "sort": {
        "orders": [
            {
                "field": "registeredOn",
                "direction": "DESC"
            }
        ]
    },
    "stages": []
}

def save_data_to_excel(data, file_name):
    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=["name", "dippNumber", "id", "industries", "sectors", "state", "city", "stages", "dippRecognitionStatus"])

    # Convert list-type columns to string
    list_columns = ["industries", "sectors", "stages", "dippRecognitionStatus"]
    for col in list_columns:
        df[col] = df[col].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

    # Generate 'page_url' based on the 'id' column
    df['page_url'] = df['id'].apply(lambda x: f"https://www.startupindia.gov.in/content/sih/en/profile.Startup.{x}.html")

    # Generate 'API_urls' based on the 'id' column
    apis_url = 'https://api.startupindia.gov.in/sih/api/common/replica/user/profile/'
    df['API_urls'] = df['id'].apply(lambda x: apis_url + str(x))

    # Merge 'state' and 'city' columns into 'location'
    df['location'] = df.apply(lambda row: f"{row['state']}, {row['city']}" if pd.notna(row['city']) else row['state'], axis=1)

    # Drop unnecessary columns
    df = df.drop(columns=['state', 'city'])

    # Check if the file already exists
    if os.path.exists(file_name):
        # Append data to the existing file
        existing_df = pd.read_excel(file_name)
        combined_df = pd.concat([existing_df, df])
        combined_df.to_excel(file_name, index=False)
    else:
        # Create a new file with the data
        df.to_excel(file_name, index=False)
        print(f"Data saved to {file_name}")



def fetch_all_data_for_state(state_id, state_name):
    all_data = []
    
    page_num = 0
    folder_name = 'test_09_09_24'
    os.makedirs(folder_name, exist_ok=True)  # Create the folder if it doesn't exist
    file_name = os.path.join(folder_name, f"{state_name}.xlsx")
    
    while True:
        payload = payload_template.copy()
        payload["states"] = [state_id]
        payload["page"] = page_num
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json().get("content", [])
            if not data:
                break  # Exit the loop if no more data is returned
            all_data.extend(data)
            print(f"Fetched page {page_num} for state: {state_name}")
            save_data_to_excel(data, file_name)  # Save data for the current page
            page_num += 1
            time.sleep(3)
        else:
            print(f"Request failed with status code: {response.status_code} for state: {state_name} on page: {page_num}")
            break
                          
    if not all_data:
        print(f"No data found for state: {state_name}")

# Read state IDs from the provided Excel sheet  
state_data = pd.read_excel(r"C:\Users\Premkumar.8265\Desktop\sui\state_id_part1.xlsx")

# Iterate through each state ID and fetch data
for index, row in state_data.iterrows():
    state_name = row['state']
    state_id = row['state_id']
    fetch_all_data_for_state(state_id, state_name)  

print("Data fetching and saving completed.")
