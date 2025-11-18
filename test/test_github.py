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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    opts = Options()

    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(options=opts)
    yield driver

    driver.quit()


def test_selenium_web(driver):
    url = "https://www.selenium.dev/"
    driver.get(url)
    assert driver.title == "Selenium"
    assert driver.current_url == url
