from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import *
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import *


def launch_driver(chrome_location):
    '''

    :param chrome_location: provide the location of the chrome browser location
    :param download_location: provide the location of the download files
    :return: It returns the driver object

    '''
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)

    # Adding argument to disable the AutomationControlled flag
    option.add_argument("--disable-blink-features=AutomationControlled")
    # option.add_argument("--headless")
    # Exclude the collection of enable-automation switches
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Turn-off userAutomationExtension
    option.add_experimental_option("useAutomationExtension", False)
    option.page_load_strategy = "eager"

    option.binary_location = chrome_location
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    # Changing the property of the navigator value for webdriver to undefined
    return driver


def load_url(driver, url):
    '''
    :param url: provide the url which needs to be loaded
    :return: Void
    '''
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)


def fluent_wait(driver, xpath):
    '''
    It will till the given xpath element is visible. Here it will 60 seconds, and it will poll for every 5
    seconds ignoring the exception
    :param driver:
    :param xpath: Provide the xpath of the element
    :return:
    '''
    wait = WebDriverWait(driver, 60, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))


def click_on_element(driver, xpath):
    '''
    It will click on the given xpath and the loop will trigger if there is any click element interception or
    stale element exception
    :param xpath: Provide the xpath of the element
    :return: Void
    '''
    try:
        driver.find_element(By.XPATH, xpath).click()

    except ElementClickInterceptedException:
        for i in range(0, 200):
            try:
                driver.find_element(By.XPATH, xpath).click()
                break
            except Exception:
                pass

    except StaleElementReferenceException:
        for i in range(0, 200):
            try:
                driver.find_element(By.XPATH, xpath).click()
                break
            except Exception:
                pass

def click_on_element_wait(driver, xpath):
    '''
    It will click on the given xpath and the loop will trigger if there is any click element interception or
    stale element exception
    :param xpath: Provide the xpath of the element
    :return: Void
    '''
    try:
        fluent_wait(driver, xpath)
        driver.find_element(By.XPATH, xpath).click()

    except ElementClickInterceptedException:
        for i in range(0, 200):
            try:
                driver.find_element(By.XPATH, xpath).click()
                break
            except Exception:
                pass

    except StaleElementReferenceException:
        for i in range(0, 200):
            try:
                driver.find_element(By.XPATH, xpath).click()
                break
            except Exception:
                pass

def getText(driver, xpath):
    try:
        text = driver.find_element(By.XPATH, xpath).text
    except:
        text = None
    return text

def getattribute(driver, xpath):
    try:
        text = driver.find_element(By.XPATH, xpath).get_attribute("href")
    except:
        text = ""
    return text

def getText1(driver, xpath):
    try:
        fluent_wait(driver, xpath)
        text = driver.find_element(By.XPATH, xpath).text
    except:
        text = ""
    return text

def fluent_wait1(driver, xpath):
    '''
    It will till the given xpath element is visible. Here it will 60 seconds, and it will poll for every 5
    seconds ignoring the exception
    :param driver:
    :param xpath: Provide the xpath of the element
    :return:
    '''
    wait = WebDriverWait(driver,30).until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))