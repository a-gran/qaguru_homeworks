import pytest
from selenium import webdriver
import time

@pytest.mark.selenium
def test_selenium():
    driver = webdriver.Chrome()
    URL = 'https://www.github.com/'
    driver.get(URL)

    time.sleep(5) # чтобы браузер не сразу закрывался

    assert driver.title == 'GitHub'
    assert driver.current_url == URL