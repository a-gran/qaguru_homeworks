from typing import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.fixture
def driver() -> Generator[WebDriver, None, None]:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(options=opts)
    yield driver

    driver.quit()


@pytest.mark.google
def test_google(driver: WebDriver) -> None:
    url = "https://www.google.com/"
    driver.get(url)

    assert driver.current_url == url
    assert driver.title == "Google"
