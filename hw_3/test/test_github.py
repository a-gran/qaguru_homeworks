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


@pytest.mark.github
def test_github(driver: WebDriver) -> None:
    url = "https://github.com/"
    driver.get(url)

    assert "GitHub" in driver.title
    assert driver.current_url == url
