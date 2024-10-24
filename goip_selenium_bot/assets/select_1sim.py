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
    await asyncio.sleep(2)

async def wait_for_element(driver, by, value, timeout=10):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        WebDriverWait(driver, timeout).until,
        EC.presence_of_element_located((by, value))
    )

async def perform_login(driver, username, password):
    loop = asyncio.get_event_loop()

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
    
def extract_phone_number(data):
    phone_pattern = re.compile(r'\+\d{12}')  # Шаблон для номера телефона в формате +380XXXXXXXXX
    match = phone_pattern.search(data)  # Ищем номер телефона в строке
    
    return match.group(0) if match else None 

async def interact_with_page(driver, select_channel):
    loop = asyncio.get_event_loop()
    
    formatted_channel = select_channel.replace('.', '_')  

    await visit_url(driver, config.gateway_ip + "goip_ussd_en.html")
    await asyncio.sleep(2)

    await loop.run_in_executor(executor, driver.find_element(By.CSS_SELECTOR, "td:nth-child(6) > input:nth-child(2)").click)
    await asyncio.sleep(1)

    input_checkbox_id = f"ID_CbxUssd{formatted_channel}" 
    try:
        await loop.run_in_executor(executor, driver.find_element(By.ID, input_checkbox_id).click)
    except Exception as e:
        print(f"Ошибка при нажатии на элемент {input_checkbox_id}: {e}")
        
    input_cmd_id = f"ID_TxaUssdCmd_{formatted_channel}"  
    try:
        ussd_input = await loop.run_in_executor(executor, lambda: driver.find_element(By.ID, input_cmd_id))
        
        await loop.run_in_executor(executor, lambda: ussd_input.clear())

        await loop.run_in_executor(executor, lambda: ussd_input.send_keys(config.ussd_code))

    except Exception as e:
        print(f"Ошибка при работе с элементом {input_cmd_id}: {e}")
        
    button_xpath = f"//input[@onclick=\"return sendUssd('{select_channel}');\"]"
    try:
        ussd_button = await loop.run_in_executor(executor, lambda: driver.find_element(By.XPATH, button_xpath))
        
        await loop.run_in_executor(executor, lambda: ussd_button.click())

    except Exception as e:
        print(f"Ошибка при поиске или нажатии на кнопку для канала {select_channel}: {e}")

    await asyncio.sleep(35)
    
    tr_id = f"ID_TrUssd_{formatted_channel}"
    textarea_value = ''
    try:
        tr_element = await loop.run_in_executor(executor, lambda: driver.find_element(By.ID, tr_id))
        textarea_element = await loop.run_in_executor(executor, lambda: tr_element.find_element(By.XPATH, "./td[5]/textarea"))
        textarea_value = await loop.run_in_executor(executor, lambda: textarea_element.get_attribute("value"))
    except Exception as e:
        print(f"Ошибка при поиске или нажатии на текстовое поле канала {select_channel}: {e}")
        
    return textarea_value

    
async def run_all(channel):
    driver = await setup_driver()
    db = Database()
    
    try:
        await visit_url(driver, config.gateway_ip)
        await wait_for_element(driver, By.ID, "id_login_box")
        await perform_login(driver, config.gateway_login, config.gateway_password)
        data = extract_phone_number(await interact_with_page(driver, channel))
        # db.add_numbers_active(filtered_data)
    finally:
        driver.quit()
        return data
        

if __name__ == "__main__":
    asyncio.run(run_all())
