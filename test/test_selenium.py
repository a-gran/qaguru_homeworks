import time

import pytest
from selenium import webdriver


@pytest.mark.selenium
def test_selenium():
    driver = webdriver.Chrome()
    URL = "https://www.selenium.dev/"
    driver.get(URL)

    time.sleep(2)  # чтобы браузер не сразу закрывался

    assert driver.current_url == URL
    assert driver.title == "Selenium"
