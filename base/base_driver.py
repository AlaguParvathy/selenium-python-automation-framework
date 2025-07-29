import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utilities.utils import Utils


class BaseDriver:
    log = Utils.custom_logger()
    def __init__(self, driver):
        self.driver = driver

    def page_scroll(self):
        pageLength = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var pageLength=document.body.scrollHeight;return pageLength;")
        match = False
        while (match == False):
            lastCount = pageLength
            time.sleep(1)
            pageLength = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var pageLength=document.body.scrollHeight;return pageLength;")
            if lastCount == pageLength:
                match = True
        self.log.info("Page scroll complete")
        time.sleep(4)

    def wait_until_element_is_clickable(self, locator_type, locator):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((locator_type,locator)))
        return element

    def wait_for_presence_of_all_elements(self,locator_type, locator):
        list_of_elements = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((locator_type,locator)))
        return list_of_elements