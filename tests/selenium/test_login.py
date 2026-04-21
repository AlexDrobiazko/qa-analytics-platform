from selenium import webdriver
from selenium.webdriver.common.by import By


def test_login_success():
    driver = webdriver.Chrome()
    try:
        driver.get("http://127.0.0.1:8010/demo/login")

        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin")
        driver.find_element(By.TAG_NAME, "button").click()

        assert "Login successful" in driver.page_source
    finally:
        driver.quit()


def test_login_fail():
    driver = webdriver.Chrome()
    try:
        driver.get("http://127.0.0.1:8010/demo/login")

        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("wrong")
        driver.find_element(By.TAG_NAME, "button").click()

        assert "Login failed" in driver.page_source
    finally:
        driver.quit()