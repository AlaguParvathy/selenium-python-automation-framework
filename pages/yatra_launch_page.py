import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from pages.search_flights_results_page import SearchFlightsResults
from utilities.utils import Utils

class LaunchPage(BaseDriver): #here Launch Page is the child of the BaseDriver class
    log = Utils.custom_logger()
    def __init__(self, driver):
        super().__init__(driver) #this initializes the super class and makes the parent class's methods available here
                                 #here we use 'driver' in the bracket because the parent class uses/accepts that as one of the arguments
        self.driver = driver
        #self.ex_wait = ex_wait

    # Externalize the locators
    LOGIN_INFO = "//span[@class='commonModal__close']"
    DEPART_FROM_FIELD = "//input[@id='fromCity']"
    DEPART_FROM_FIELD_NEXT = "//input[@placeholder='From']"
    DEPART_FROM_RESULT_LIST = "//li[contains(@id, 'react-autowhatever')"
    GOING_TO_FIELD = "//label[@for='toCity']"
    GOING_TO_FIELD_NEXT = "//input[@placeholder='To']"
    GOING_TO_RESULT_LIST = "//li[contains(@id, 'react-autowhatever"
    SELECT_DATE_FIELD = "//p[@data-cy='departureDate']"
    ALL_DATES = "//div[contains(@class,'DayPicker-Day')]"
    SEARCH_BUTTON = "//a[@class='primaryBtn font24 latoBold widgetSearchBtn ']"

    #Since all the locators and the corresponding actions should be in the same page class
    def get_login_info_pop_up(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.LOGIN_INFO)

    def get_depart_from_field(self):
        return self.driver.find_element(By.XPATH, self.DEPART_FROM_FIELD)

    def get_depart_from_field_next(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.DEPART_FROM_FIELD_NEXT)

    def get_depart_from_result_field(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.DEPART_FROM_RESULT_LIST)

    def get_going_to_field(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.GOING_TO_FIELD)

    def get_going_to_field_next(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.GOING_TO_FIELD_NEXT)

    def get_going_to_result_field(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.GOING_TO_RESULT_LIST)

    def select_date_field(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.SELECT_DATE_FIELD)

    def get_all_dates(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.ALL_DATES)

    def get_search_button(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.SEARCH_BUTTON)

    #actual methods to perform the operations
    def enter_depart_from_location(self, depart_location):
        self.get_login_info_pop_up().click()
        self.get_depart_from_field_next().click()
        self.log.info("clicked on depart from")
        time.sleep(2)
        self.get_depart_from_field_next().send_keys(depart_location)
        self.log.info("Typed text into depart from successfully")
        search_results = self.get_depart_from_result_field()
        print(len(search_results))
        for results in search_results:
            if depart_location in results.text:
                time.sleep(4)
                results.click()
                break

    def enter_going_to_location(self, going_to_location):
        self.get_going_to_field().click()
        self.log.info("clicked on going")
        time.sleep(2)
        self.get_going_to_field_next().send_keys(going_to_location)
        self.log.info("Typed text into going to field successfully")
        search_results = self.get_going_to_result_field()
        print(len(search_results))
        for results in search_results:
            if going_to_location in results.text:
                time.sleep(4)
                results.click()
                break

    def enter_departure_date(self, depart_date):
        element = self.select_date_field()
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(2)
        all_dates = self.get_all_dates().find_elements(By.XPATH, self.ALL_DATES)
        for sel_dates in all_dates:
            label = sel_dates.get_attribute("aria-label")
            if label is None:
                continue
            if depart_date in label:
                sel_dates.click()
                break

    def click_search_flights_button(self):
        self.get_search_button().click()
        time.sleep(3)

    def consolidated_search_flights(self,depart_location, going_to_location, depart_date):
        self.enter_depart_from_location(depart_location)
        self.enter_going_to_location(going_to_location)
        self.enter_departure_date(depart_date)
        self.click_search_flights_button()
        #creating an object for the next flight to make connections between the pages
        search_flights_results_page_object = SearchFlightsResults(self.driver)
        return search_flights_results_page_object

    #the below code is the one before optimization
    # def departfrom(self, depart_location):
    #     self.driver.find_element(By.XPATH, "//p[normalize-space()='DEL, Indira Gandhi International']").click()
    #     depart_from = self.wait_until_element_is_clickable(By.XPATH, "//input[@id='input-with-icon-adornment']")
    #     depart_from.send_keys(depart_location)
    #     self.driver.find_element(By.XPATH, "//div[contains(@class,'fw-600 mb-0')]").click()

    # def goingto(self, destination_location):
    #     self.driver.find_element(By.XPATH, "//p[normalize-space()='BOM, Chhatrapati Shivaji International']").click()
    #     arrive_at = self.wait_until_element_is_clickable(By.XPATH, "//input[@id='input-with-icon-adornment']")
    #     arrive_at.send_keys(destination_location)
    #     time.sleep(3)
    #     search_results = self.driver.find_elements(By.XPATH, "//div[contains(@class,'MuiStack-root css-1187icl')]//div[1]//div[1]//div//li")
    #
    #     print(len(search_results))
    #     for results in search_results:
    #         if "New York" in results.text:
    #             time.sleep(4)
    #             results.click()
    #             break

    # def selectdate(self, departure_date):
    #     self.driver.find_element(By.XPATH, "//div[@aria-label='Departure Date inputbox']//div[2]").click()
    #     time.sleep(2)
    #     all_dates = self.wait_until_element_is_clickable(By.XPATH,"//div[@class = 'react-datepicker__month']//div[@class='react-datepicker__week']//div[@aria-disabled='false']").find_elements(By.XPATH,
    #                                           "//div[@class = 'react-datepicker__month']//div[@class='react-datepicker__week']//div[@aria-disabled='false']")
    #     for sel_dates in all_dates:
    #         if departure_date in sel_dates.get_attribute("aria-label"):
    #             sel_dates.click()
    #             break

    # def clicksearch(self):
    #     self.driver.find_element(By.XPATH, "//button[normalize-space()='Search']").click()
    #     time.sleep(5)