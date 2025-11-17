import time

import pytest
from selenium import webdriver


@pytest.mark.github
def test_github():
    driver = webdriver.Chrome()
    URL = "https://github.com/"
    driver.get(URL)

    time.sleep(2)  # чтобы браузер не сразу закрывался

    assert driver.current_url == URL
    assert "GitHub" in driver.title
