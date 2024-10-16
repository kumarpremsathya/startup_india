from selenium import webdriver
from datetime import datetime
import mysql.connector

source_status = "Active"

download_folder = r"C:\Users\magudapathy.7409\Desktop\sui_test_incre\incremental_start_up_india\data\excel_sheet"


def browser_configure():
    chrome_options = webdriver.ChromeOptions()
    chrome_prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": download_folder,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)
    browser = webdriver.Chrome(options=chrome_options)
    return browser


log_list = [None] * 14
no_data_avaliable = 0
no_data_scraped = 0
deleted_sources = ""
newly_added= 0
updated_count = 0
total_deleted_count = 0
new_deleted_sources = []
new_deleted_count = 0
checking_data_in_database = 0
source_name = "startupIndia"
table_name = "sui_final"


# host = '4.213.77.165'
# user = 'root1'
# password = 'Mysql1234$'
# database = 'startup_india'

host = 'localhost'
user = 'root'
password = 'root'
database = 'startup'

current_date = datetime.now().strftime("%Y-%m-%d")


def db_connection():
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return connection
