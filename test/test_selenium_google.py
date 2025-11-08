import time

import pytest
from selenium import webdriver


# @pytest.mark.only
@pytest.mark.google
def test_selenium():
    driver = webdriver.Chrome()
    URL = "https://www.google.com/"
    driver.get(URL)

    time.sleep(2)  # чтобы браузер не сразу закрывался

    assert driver.current_url == URL
