import time

import pytest
from selenium import webdriver


@pytest.mark.github
def test_selenium():
    driver = webdriver.Chrome()
    URL = "https://www.github.com/"
    driver.get(URL)

    time.sleep(2)  # чтобы браузер не сразу закрывался

    assert driver.title == "GitHub"
    assert driver.current_url == URL
