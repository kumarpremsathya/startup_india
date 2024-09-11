
#company url getting script
import time
import traceback
import data_provider
from sqlalchemy import create_engine
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import driverUtil
from data_provider import *
from selenium.webdriver.common.by import By

from datetime import datetime
from selenium import webdriver

def current_date_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

start_row_no =0
end_row_no = 1000
                                              
config = data_provider.convert_to_dict_from_excel("SmartIndiaData.xlsx", "key", "value")

chrome_location = config["chrome_location"]
DPIITRecognisedStartups = config["DPIITRecognisedStartups"]
IA80CExemptedStartups = config["80IACExemptedStartups"]
totalCountXpath = config["totalCountXpath"] 
companyTitleXpath = config["companyTitleXpath"]
loadMore = config["loadMore"]
stageXpath = config["stageXpath"]
focusIndustryXpath = config["focusIndustryXpath"]
focusSectorXpath = config["focusSectorXpath"]
serviceAreaXpath = config["serviceAreaXpath"]
locationXpath = config["locationXpath"]
noOfYearXpath = config["noOfYearXpath"]
companyURLXpath = config["companyURLXpath"]
aboutDetailsXpath = config["aboutDetailsXpath"]
joinedDateXpath = config["joinedDateXpath"]
DPIITRecognisedXpath = config["DPIITRecognisedXpath"]
activeSinceXpath = config["activeSinceXpath"]
companyTitleXpathNew = config["companyTitleXpathNew"]

hostIpAddress = config["hostIpAddress"]
db_userName = config["db_userName"]
db_password = config["db_password"]
db_name = config["db_name"]
# mydb = data_provider.database_connection(hostIpAddress, db_userName, db_password, db_name)

driver = webdriver.Chrome()
# driverUtil.load_url(driver, "https://www.startupindia.gov.in/content/sih/en/search.html?roles=Startup&page=0#")

# dbConnection = create_engine(config["db_data1"])
input_df = pd.read_excel(r"C:\Users\Premkumar.8265\Desktop\startup\incremental_pageurls_09_09_2024.xlsx")
print(input_df)
# df = data_provider.database_to_df(dbConnection, 'start_up_india')
# df_new = data_provider.database_to_df(dbConnection, 'startup_demo')
# print(df)
# print(df_new)
all_data = []

for i, j in input_df["pageurl"].items():
   
    data = []
    if i > end_row_no:
        break


    if i < start_row_no:
            continue

    driverUtil.load_url(driver, str(j))

    try:
        stage = driverUtil.getText(driver, stageXpath)
    except:
        print("error occured")
        print(traceback.print_exc())
        driver.get('chrome://settings/clearBrowserData')

        action = ActionChains(driver)
        action.send_keys(Keys.TAB).perform()
        action.send_keys(Keys.ENTER).perform()
        driverUtil.load_url(driver, j)
        stage = driverUtil.getText(driver, stageXpath)
        
    counter = 0

    while stage is None:

        time.sleep(2)
        stage = driverUtil.getText(driver, stageXpath)
        print("error occured")
        counter = counter+1

        if counter > 10:
             break

    
    companyTitle = driverUtil.getText(driver, companyTitleXpathNew)
    focusIndustry = driverUtil.getText(driver, focusIndustryXpath)
    focusSector = driverUtil.getText(driver, focusSectorXpath)
    serviceArea = driverUtil.getText(driver, serviceAreaXpath)
    location = driverUtil.getText(driver, locationXpath)
    noOfYear = driverUtil.getText(driver, noOfYearXpath)
    companyURL = driverUtil.getText(driver, companyURLXpath)
    aboutDetails = driverUtil.getText(driver, aboutDetailsXpath)
    joinedDate = driverUtil.getText(driver, joinedDateXpath)
    DPIITRecognised = driverUtil.getText(driver, DPIITRecognisedXpath)
    activeSince = driverUtil.getText(driver, activeSinceXpath)

    # data.append(i)
    data.append("DPIITRecognisedStartups")
    # data.append(IA80CExemptedStartups)
    # data.append(totalCount)
    data.append(companyTitle)
    data.append(stage)
    data.append(focusIndustry)
    data.append(focusSector)
    data.append(serviceArea)
    data.append(location)
    data.append(noOfYear)
    data.append(companyURL)
    data.append(aboutDetails)
    data.append(joinedDate)
    data.append(DPIITRecognised)
    data.append(activeSince)
    data.append(str(j))
    data.append(None)
    data.append(current_date_time())
    # data.append("date")

    # data = [data]

    column_names = ["DPIIT", "companyName", "stage", "focusIndustry", "focusSector", "serviceArea", "location",
                        "noOfYear", "companyURL", "aboutDetails", "joinedDate", "DPIITRecognised", "activeSince","pageurl","Updated_date","dateofScrapping"]
    
    # print(len(column_names))

    print(data[0][1])

    # query = f"INSERT INTO start_demo (S. No,DPIIT,companyName,stage,focusIndustry,focusSector,serviceArea,location,noOfYear,companyURL,aboutDetails,joinedDate,DPIITRecognised,activeSince,dateofScrapping) values({i},{data[0]},{companyTitle},{stage},{focusIndustry},{focusSector},{serviceArea},{location},{noOfYear},{companyURL},{aboutDetails},{joinedDate},{DPIITRecognised},{activeSince},dateofScrapping)"
    # print(query)
    # data_provider.execute_query(mydb, query)
    # data_provider.commit_to_db(mydb)
    all_data.append(data)
    new_df = pd.DataFrame(all_data, columns=column_names)
    new_df.to_excel('pageurl_results_09_09_2024.xlsx', index=False)

    # try:
    #      data_provider.sql_table_to_db(dbConnection, new_df, "pending_6th_api")
    # except:
    #       dbConnection = create_engine(config["db_data1"])
    #       data_provider.sql_table_to_db(dbConnection, new_df, "pending_6th_api")

    time.sleep(3)
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])

driver.quit()








import requests
import pandas as pd
import time

# Define the input and output file paths
input_file = r'C:\Users\Premkumar.8265\Desktop\startup\incremental_pageurls_09_09_2024.xlsx'
output_file = 'apiurl_results_09_09_2024.xlsx'

# Define the base URL template
baseurl = "https://www.startupindia.gov.in/content/sih/en/profile.Startup.{}.html"

# Read the URLs from the Excel file
df_urls = pd.read_excel(input_file, sheet_name='Sheet1')  # Adjust sheet_name if needed
urls = df_urls['API_urls']

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
            
            'dipp_number': dippNumber,
            'dippRecognitionStatus': dippRecognitionStatus,
            'name': name,
            'legalName': legalName,
            'cin':cin,
            'pan':pan,
            'stateName': stateName,
            'pageurl': page_url  # Add the page URL to the results
        })
        time.sleep(3) 
        # Save to Excel after each request
        df_results = pd.DataFrame(results)
        df_results.to_excel(output_file, index=False, engine='openpyxl')
        
        # Wait for 3 seconds before the next request
       

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

print(f"Data has been saved to {output_file}")



# Merge DataFrames on 'pageurl'
merged_df = pd.merge(new_df, df_results, on='pageurl', how='left')


# Desired column order
desired_columns = [
    'DPIIT', 'companyName', 'stage', 'focusIndustry', 'focusSector', 'serviceArea',
    'location', 'noOfYear', 'companyURL', 'aboutDetails', 'joinedDate',
    'DPIITRecognised', 'activeSince', 'pageurl', 'Updated_date', 'dipp_number',
    'legalName', 'cin', 'pan', 'dateofScrapping'
]

# Reorder columns
merged_df = merged_df[desired_columns]

# Save merged data to a new Excel file
merged_file_path = 'combined_page_apiurls_09_09_2024.xlsx'
merged_df.to_excel(merged_file_path, index=False)





pre_final_df = pd.read_excel(r"C:\Users\Premkumar.8265\Desktop\startup\merged_output_09_09_2024.xlsx")

# merged_df = pd.read_excel(r"C:\Users\Premkumar.8265\Desktop\startup\combined_page_apiurls.xlsx")

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

final_file_path = 'final_excels_09_09_2024.xlsx'
final_df.to_excel(final_file_path, index=False)


print(f"Data has been saved to {final_file_path}")






