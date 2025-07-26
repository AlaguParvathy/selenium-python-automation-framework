import time
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.utils import Utils
import logging


class SearchFlightsResults(BaseDriver):
    log = Utils.custom_logger(logLevel=logging.WARNING)
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        #self.ex_wait = ex_wait

    #Externalize the locators
    ONE_STOP_RADIO_BUTTON = "The xpath to click the checkbox that filters 1 stops"
    TWO_STOP_RADIO_BUTTON = "The xpath to click the checkbox that filters 1 stops"
    NON_STOP_RADIO_BUTTON = "The xpath to click the checkbox that filters 1 stops"
    SEARCH_FLIGHTS_RESULTS = "The xpath the get the all flights present in the result page after selecting no. of stops"

    def get_one_stop_radio_button(self):
        return self.driver.find_element(By.XPATH, self.ONE_STOP_RADIO_BUTTON)

    def get_two_stop_radio_button(self):
        return self.driver.find_element(By.XPATH, self.TWO_STOP_RADIO_BUTTON)

    def get_non_stop_radio_button(self):
        return self.driver.find_element(By.XPATH, self.NON_STOP_RADIO_BUTTON)

    def get_search_flight_results(self):
        return self.wait_for_presence_of_all_elements(By.XPATH,self.SEARCH_FLIGHTS_RESULTS)

    def filter_flights_by_stops(self, by_stop):
        if by_stop == '1Stop':
            self.get_one_stop_radio_button().click()
            self.log.warning("Selected flights with 1 Stop")
            time.sleep(2)

        elif by_stop == '2 Stop':
            self.get_two_stop_radio_button().click()
            self.log.warning("Selected flights with 2 Stop")
            time.sleep(2)

        elif by_stop == 'Non Stop':
            self.get_non_stop_radio_button().click()
            self.log.warning("Selected flights non-stop Stop")
            time.sleep(2)

        else:
            self.log.warning("Please provide valid filter option")

    #the code before optimization
    # def filter_flights(self):
    #     self.driver.find_element(By.XPATH,"The xpath to click the checkbox that filters 1 stops").click()
    #     time.sleep(4)


