import time
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.utils import Utils
import logging


class SearchFlightsResults(BaseDriver):
    log = Utils.custom_logger()
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        #self.ex_wait = ex_wait

    #Externalize the locators
    ONE_STOP_RADIO_BUTTON = "//p[@class='checkboxTitle'][contains(text(),'1 Stop')]"
    TWO_STOP_RADIO_BUTTON = "The xpath to click the checkbox that filters 2 stops"
    NON_STOP_RADIO_BUTTON = "//p[@class='checkboxTitle'][contains(text(),'Non Stop')]"
    SEARCH_FLIGHTS_RESULTS = "//p[@class='flightsLayoverInfo']"

    def scroll_to_stop_checkboxes(self, element_xpath):
        element = self.wait_until_element_is_clickable(By.XPATH, element_xpath)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)

    def get_one_stop_radio_button(self):
        self.scroll_to_stop_checkboxes(self.ONE_STOP_RADIO_BUTTON)
        self.log.info("scrolled to the checkbox")
        return self.wait_until_element_is_clickable(By.XPATH, self.ONE_STOP_RADIO_BUTTON)

    def get_two_stop_radio_button(self):
        self.scroll_to_stop_checkboxes(self.TWO_STOP_RADIO_BUTTON)
        self.log.info("scrolled to the checkbox")
        return self.wait_until_element_is_clickable(By.XPATH, self.TWO_STOP_RADIO_BUTTON)

    def get_non_stop_radio_button(self):
        self.scroll_to_stop_checkboxes(self.NON_STOP_RADIO_BUTTON)
        self.log.info("scrolled to the checkbox")
        return self.wait_until_element_is_clickable(By.XPATH, self.NON_STOP_RADIO_BUTTON)

    def get_search_flight_results(self):
        return self.wait_for_presence_of_all_elements(By.XPATH,self.SEARCH_FLIGHTS_RESULTS)

    def filter_flights_by_stops(self, by_stop):

        if by_stop == '1 stop':
            self.get_one_stop_radio_button().click()
            self.log.info("Selected flights with 1 Stop")
            time.sleep(2)

        elif by_stop == '2 stop':
            self.get_two_stop_radio_button().click()
            self.log.info("Selected flights with 2 Stop")
            time.sleep(2)

        elif by_stop == 'Non stop':
            self.get_non_stop_radio_button().click()
            self.log.info("Selected flights non-stop Stop")
            time.sleep(2)

        else:
            self.log.warning("Please provide valid filter option")

    #the code before optimization
    # def filter_flights(self):
    #     self.driver.find_element(By.XPATH,"The xpath to click the checkbox that filters 1 stops").click()
    #     time.sleep(4)


