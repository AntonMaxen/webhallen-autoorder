import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.webhallen.com/se/product/324469-Hyrule-Warriors-Age-of-Calamity')
phonenumber = "0812101237"

delay = 7

try:
    button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='btn btn-white p-5 m-4 stretch-x'")))
    button.click()
except TimeoutException:
    print("Loading took to much time.")


try:
    #find button to add to cart
    container = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "add-product-to-cart")))
    button = container.find_element_by_tag_name("button")
    button.click()
    button.click()
    # find button to checkout
    b = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='btn stretch-x mb-5 btn-primary")))
    b.click()

    # find a way to redo this TODO
    box = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='col-xs-6 p-5 text-center border-right clickable gray-on-hover'")))
    box.click()

    # Look for search section
    search_section = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "search-section")))
    search_input = WebDriverWait(search_section, delay).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    search_input.send_keys('44230')

    time.sleep(1)
    # Look for button that sends search input
    search_button = WebDriverWait(search_section, delay).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
    search_button.click()

    # Find a better way to wait for search to update TODO
    time.sleep(1)

    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    correct_location = False
    while not correct_location:
        search_section = WebDriverWait(driver, delay, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.ID, "search-section")))
        print("lööp")
        search_button = WebDriverWait(search_section, delay, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
        # a
        first_location = WebDriverWait(search_section, delay, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.TAG_NAME, "li")))
        print(first_location)
        store_div = WebDriverWait(first_location, delay, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CLASS_NAME, "store-name")))
        print(store_div)
        text_div = WebDriverWait(store_div, delay, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.TAG_NAME, "div")))
        print(text_div.text)
        if "Nordstan" in text_div.text:
            first_location.click()
            correct_location = True
        else:
            search_button.click()


except TimeoutException:
    print("Took to long time")
    print(TimeoutException)



def main():
    pass


if __name__ == '__main__':
    main()
