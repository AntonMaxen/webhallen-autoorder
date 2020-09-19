import time
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from order import order_product


def close_popup(driver, delay, selector):
    try:
        button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        button.click()
    except TimeoutException:
        print("took to much time")


def find_element_by_id(driver, delay, selector):
    try:
        element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, selector)))
        return element
    except TimeoutException:
        print("Took to much time")

def find_clickable_by_tagname(driver, delay, selector):
    try:
        element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.TAG_NAME, selector)))
        return element
    except TimeoutException:
        print("took to much time")

def product_available(url, rate, delay=30):
    print("checker is running.")
    options = webdriver.ChromeOptions()
    options.add_argument('--no-proxy-server')
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    #options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)

    available = False
    while not available:
        container = find_element_by_id(driver, delay, "add-product-to-cart")
        button = find_clickable_by_tagname(container, delay, "button")
        print(button.text)
        print(datetime.datetime.now())
        if "Meddela" not in button.text:
            available = True
        else:
            time.sleep(rate)
            driver.refresh()

    return available


def main():
    url = "https://www.webhallen.com/se/product/323402-Webhallen-Config-D20-0306-i7-10700K-16GB-RAM-1TB-SSD-RTX-3080-Win-10"
    url2 = "https://www.webhallen.com/se/product/324469-Hyrule-Warriors-Age-of-Calamity"
    url3 = "https://www.webhallen.com/se/product/314219-Lenovo-G34w-10-34-QHD-4ms-144Hz-DP-HDMI-Justerbar-FreeSync-VESA"
    delay = 30
    refresh_rate = 2

    order_url = url
    if product_available(order_url, refresh_rate, delay):
        driver = order_product(order_url, delay)
    else:
        print("something happened")

    return driver


if __name__ == '__main__':
    driver = main()
