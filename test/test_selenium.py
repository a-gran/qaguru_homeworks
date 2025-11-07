import pytest
from selenium import webdriver
import time


@pytest.mark.selenium
def test_selenium():
    driver = webdriver.Chrome()
    URL = "https://www.selenium.dev/"
    driver.get(URL)

    time.sleep(5)  # чтобы браузер не сразу закрывался

    assert driver.title == "Selenium"
    assert driver.current_url == URL
