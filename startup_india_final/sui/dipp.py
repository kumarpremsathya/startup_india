import requests
import pandas as pd
import time

# Define the input and output file paths
input_file = r'C:\Users\Premkumar.8265\Desktop\sui\excel_file_updated.xlsx'
output_file = 'startup_details_all_pending.xlsx'

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
        time.sleep(2)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Extract the required fields
        dippNumber = data['user']['startup']['dippNumber']
        dippRecognitionStatus = data['user']['startup']['dippRecognitionStatus']
        name = data['user']['name']
        uniqueId = data['user']['uniqueId']

        # Append the extracted data to the results list
        results.append({
            'dippNumber': dippNumber,
            'dippRecognitionStatus': dippRecognitionStatus,
            'name': name,
            'uniqueId': uniqueId
        })
        
        # Save to Excel after each request
        df_results = pd.DataFrame(results)
        df_results.to_excel(output_file, index=False, engine='openpyxl')
        
        # Wait for 3 seconds before the next request
        time.sleep(3)

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

print(f"Data has been saved to {output_file}")