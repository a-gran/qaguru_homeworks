import pytest
from selenium import webdriver
import time

@pytest.mark.selenium
def test_selenium():
    driver = webdriver.Chrome()
    URL = 'https://www.google.com/'
    driver.get(URL)

    time.sleep(3) # чтобы браузер не сразу закрывался

    assert driver.current_url == URL