import os

from selenium import webdriver
#imports for chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
#imports for firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
#imports for edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import pytest
import time

@pytest.fixture(scope="class")
#as we will be calling this fixture in another class we have to define the scope as "class"
def setUp(request, browser, url):
        if browser == "chrome":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif browser == "firefox":
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        elif browser == "edge":
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        # we are optimizing the wait so we are commenting this out
        # ex_wait = WebDriverWait(driver, 10)
        driver.get(url)
        driver.maximize_window()
        # we are returning this driver at a class level
        request.cls.driver = driver
        # request.cls.ex_wait = ex_wait
        yield
        driver.close()

def pytest_addoption(parser):
    #to pass the type of browser as argument
    parser.addoption("--browser")
    #to pass test url as argument
    parser.addoption("--url")

#fixture for browser
@pytest.fixture(scope="session", autouse=True)
def browser(request):
    return request.config.getoption("--browser")

#fixture for url
def url(request):
    return request.config.getoption("--url")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        # always add url to report
        extra.append(pytest_html.extras.url("provide the url you want to append on the report"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            report_directory = os.path.dirname(item.config.option.htmlpath)
            file_name = str(int(round(time.time() * 1000))) + ".png"
            # file_name = report.nodeid.replace("::", "_") + ".png"
            destinationFile = os.path.join(report_directory, file_name)
            driver.save_screenshot(destinationFile)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:300px;height=200px" ' \
                       'onclick="window.open(this.src)" align="right"/></div>'%file_name
            extra.append(pytest_html.extras.html(html))
        report.extra = extra

def pytest_html_report_title(report):
    report.title = "Automation Report"
