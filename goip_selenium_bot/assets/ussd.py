import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import re

from config_reader import config
from database.db import *

executor = ThreadPoolExecutor()

async def setup_driver():
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")

    loop = asyncio.get_event_loop()
    driver = await loop.run_in_executor(executor, webdriver.Firefox, firefox_options)
    return driver

async def visit_url(driver, url):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, driver.get, url)

def extract_phone_number(data):
    formatted_data = {}
    phone_pattern = re.compile(r'\+\d{12}')  # Pattern to match a phone number in the format +380XXXXXXXXX
    
    for key, value in data.items():
        match = phone_pattern.search(value)
        formatted_data[key] = match.group(0) if match else None  # Set None if no match

    return formatted_data

async def wait_for_element(driver, by, value, timeout=10):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        WebDriverWait(driver, timeout).until,
        EC.presence_of_element_located((by, value))
    )

async def perform_login(driver, username, password):
    loop = asyncio.get_event_loop()
    await asyncio.sleep(1)

    username_field = await loop.run_in_executor(executor, driver.find_element, By.ID, 'accountID')
    password_field_visible = await loop.run_in_executor(executor, driver.find_element, By.ID, 'passwordID2')
    password_field_hidden = await loop.run_in_executor(executor, driver.find_element, By.ID, 'passwordID')

    await loop.run_in_executor(executor, username_field.click)
    await asyncio.sleep(0.5)
    await loop.run_in_executor(executor, username_field.send_keys, username)
    await loop.run_in_executor(executor, password_field_visible.click)

    await wait_for_element(driver, By.ID, 'passwordID')
    await loop.run_in_executor(executor, driver.execute_script, "arguments[0].value = arguments[1];", password_field_hidden, password)

    await asyncio.sleep(1)
    await loop.run_in_executor(executor, password_field_hidden.send_keys, Keys.RETURN)
    await asyncio.sleep(1)

async def interact_with_page(driver):
    loop = asyncio.get_event_loop()

    await visit_url(driver, config.gateway_ip + "goip_ussd_en.html")
    await asyncio.sleep(2)
    
    await loop.run_in_executor(executor, driver.find_element(By.CSS_SELECTOR, "td:nth-child(6) > input:nth-child(2)").click)
    await asyncio.sleep(0.5)


    
async def interact_with_page_step2(driver):
    loop = asyncio.get_event_loop()
    
    await loop.run_in_executor(executor, driver.find_element(By.CSS_SELECTOR, "th:nth-child(1)").click)
    await asyncio.sleep(0.5)
    await loop.run_in_executor(executor, driver.find_element(By.ID, "ID_TxaUssdCmd_All0").click)
    await asyncio.sleep(0.5)
    await loop.run_in_executor(executor, driver.find_element(By.ID, "ID_TxaUssdCmd_All0").send_keys, config.ussd_code)
    await asyncio.sleep(0.5)
    await loop.run_in_executor(executor, driver.find_element(By.CSS_SELECTOR, "td:nth-child(3) > input:nth-child(1)").click)
    await asyncio.sleep(0.5)
    await loop.run_in_executor(executor, driver.find_element(By.CSS_SELECTOR, ".listHead td:nth-child(5) > input").click)
    await asyncio.sleep(1200)

async def collect_data(driver):
    rows = driver.find_elements(By.XPATH, "//table[@id='ID_TabUssd']/tbody/tr")
    data = {}

    for row in rows:
        try:
            key = row.find_element(By.XPATH, "td[2]").text
            textarea = row.find_element(By.XPATH, "td[5]/textarea")
            value = textarea.text
        except:
            value = ""
        data[key] = value
    return data

async def run_all(only_collect=True):
    driver = await setup_driver()
    db = Database()
    
    if only_collect:
        try:
            await visit_url(driver, config.gateway_ip)
            await wait_for_element(driver, By.ID, "id_login_box")
            await perform_login(driver, config.gateway_login, config.gateway_password)
            await interact_with_page(driver)
            data = await collect_data(driver)
            filtered_data = extract_phone_number(data)
            # print(filtered_data)
            db.add_numbers(filtered_data)
        finally:
            driver.quit()
    else:
        try:
            await visit_url(driver, config.gateway_ip)
            await wait_for_element(driver, By.ID, "id_login_box")
            await perform_login(driver, config.gateway_login, config.gateway_password)
            await interact_with_page(driver)
            await interact_with_page_step2(driver)
            data = await collect_data(driver)
            filtered_data = extract_phone_number(data)
            db.add_numbers(filtered_data)
        finally:
            driver.quit()

if __name__ == "__main__":
    asyncio.run(run_all())
