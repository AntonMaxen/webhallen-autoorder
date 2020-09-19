import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def order_product(url, delay=30):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    try:
        button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='btn btn-white p-5 m-4 stretch-x'")))
        button.click()
    except TimeoutException:
        print("Loading took to much time.")

    try:
        #find button to add to cart
        container = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "add-product-to-cart")))
        button = WebDriverWait(container, delay).until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
        button.click()
        # find button to checkout

        cart_link = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for*='cart-']")))
        cart_link.click()

        cart = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='cart-large']")))
        button = WebDriverWait(cart, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/checkout']")))
        button.click()

        # find a way to redo this TODO
        box = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='col-xs-6 p-5 text-center border-right clickable gray-on-hover'")))
        box.click()

        time.sleep(1)

        link_container = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='search-mode-wrapper']")))

        show_all_link = WebDriverWait(link_container, delay).until(EC.element_to_be_clickable((By.TAG_NAME, "a")))
        show_all_link.click()

        store_selector = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='store-selector'")))

        store_groups = WebDriverWait(store_selector, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class='store-group p-2']")))

        for store_group in store_groups:
            store_group_name = WebDriverWait(store_group, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='store-group-name']")))
            if store_group_name.text in "Göteborg":
                print(store_group_name)
                break

        locations = WebDriverWait(store_group, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))

        for location in locations:
            print(location.text)
            if "Nordstan" in location.text:
                break

        location.click()

        fields = {
            "phone": "0767808015",
            "email": "Anton.maxen@gmail.com"
        }

        for name, value in fields.items():
            print(name)
            elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, name)))
            elem.send_keys(value)

        order_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='btn-lg']")))
        order_button.click()
        # driver.execute_script("arguments[0].click();", order_button)

    except TimeoutException:
        print("Took to long time")
        print(TimeoutException)
    finally:
        print("Success!")

    return driver


def main():
    url = "https://www.webhallen.com/se/product/323402-Webhallen-Config-D20-0306-i7-10700K-16GB-RAM-1TB-SSD-RTX-3080-Win-10"
    order_product(url, 100)
    pass


if __name__ == '__main__':
    main()
