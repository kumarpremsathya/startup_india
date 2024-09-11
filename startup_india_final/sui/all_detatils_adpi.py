import requests
import pandas as pd
import time

# Define the input and output file paths
input_file = r'C:\Users\Premkumar.8265\Desktop\sui\excel_file_api_old.xlsx'
output_file = 'SUI_pen.xlsx'

# Define the base URL template
baseurl = "https://www.startupindia.gov.in/content/sih/en/profile.Startup.{}.html"

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

        dippNumber = startup.get('dippNumber', 'N/A')
        dippRecognitionStatus = startup.get('dippRecognitionStatus', 'N/A')
        name = user.get('name', 'N/A')
        uniqueId = user.get('uniqueId', 'N/A')  # Still needed for URL construction
        legalName = startup.get('legalName', 'N/A')

        cin = startup.get('cin', 'N/A')
        pan = startup.get('pan', 'N/A')

        # Extract additional fields
        stateName = startup.get('location', {}).get('state', {}).get('stateName', 'N/A')


        # Construct the page URL
        page_url = baseurl.format(uniqueId)

        # Append the extracted data to the results list
        results.append({
            
            'dippNumber': dippNumber,
            'dippRecognitionStatus': dippRecognitionStatus,
            'name': name,
            'legalName': legalName,
            'cin':cin,
            'pan':pan,
            'stateName': stateName,
            'page_url': page_url  # Add the page URL to the results
        })
        time.sleep(3) 
        # Save to Excel after each request
        df_results = pd.DataFrame(results)
        df_results.to_excel(output_file, index=False, engine='openpyxl')
        
        # Wait for 3 seconds before the next request
       

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

print(f"Data has been saved to {output_file}")
