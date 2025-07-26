import pytest
import softest
from pages.yatra_launch_page import LaunchPage
from utilities.utils import Utils
from ddt import ddt,data,unpack,file_data

#this is to use the fixture defined in 'conftest.py'
@pytest.mark.usefixtures("setUp")
@ddt
class Testsearchflights(softest.TestCase):
    log = Utils.custom_logger()
    #To call these methods we shall use fixture feature from pytest
    #as 'autouse' is kept true it will be executed automatically before test method
    @pytest.fixture(autouse=True)
    def class_setup(self):
        #we use this method to create objects for all the class that we have down below
        self.yatra_launch_page_object = LaunchPage(self.driver)
        self.ut = Utils()

    # @data(("New Delhi","New York","July 29th","1 Stop"),("Bengaluru","Montreal","August 1st","2 Stop")) #these parameters are called data decorators
    # @unpack
    #to read data from an external json file
    #no needed for unpack here
    #@file_data("../testdata/testdata.json")
    #to read the data from the yaml format
    #@file_data("../testdata/testdatayaml.yaml")
    #how to read test data from excel file
    #here we use the start to show that we are expecting a list
    #@data(*Utils.read_data_from_excel("D:\\Python_Selenium\\TestFrameworkDemo\\testdata\\testdata.xlsx", "sample_data"))
    #@unpack
    #to read data from csv file
    @data(*Utils.read_data_from_csv("D:\\Python_Selenium\\TestFrameworkDemo\\testdata\\testdata.csv"))
    @unpack
    def test_search_flights_1_stop(self, goingfrom, goingto, departuredate, stops):
        #launching browser and opening the travel website
        #consolidated method to search flights with all actions in one method
        #the object was created in the above method
        #yatra_launch_page_object = LaunchPage(self.driver)
        #the below line now returns the object of the next page
        search_flights_result = self.yatra_launch_page_object.consolidated_search_flights(goingfrom, goingto, departuredate)

        #code before consolidated code optimization
        # {
        # #Provide going from location
        # lp = LaunchPage(self.driver)
        # #lp.departfrom("New Delhi")
        # #this is the improvised method
        # lp.enter_depart_from_location("New Delhi")
        #
        # #Provide going to location
        # #lp.goingto("New York")
        # lp.enter_going_to_location("New York")
        #
        # #Select the departure date
        # #lp.selectdate("July 29th")
        # lp.enter_departure_date("July 29th")
        #
        # #click on the search button
        # # lp.clicksearch()
        # lp.click_search_flights_button()
        # }

        #to handle dynamic scroll
        self.yatra_launch_page_object.page_scroll()
        #by inheriting the BaseDriver properties in the child class
        #we don't have to create a separate object for the BaseDriver class here
        #instead we can use the child object to access the methods

        #Select the filter 1 stop
        #now to optimize further we move this object to the 'yatra launch page'
        # search_flights_results_page_object = SearchFlightsResults(self.driver)
        search_flights_result.filter_flights_by_stops(stops)
        #old code before optimization
        #sf.filter_flights()

        #get list of all flights that showed up in the results page after selecting the number of stops
        all_stops = search_flights_result.get_search_flight_results()
        self.log.info(all_stops)

        # verify that the filtered results show flights only 1 stop
        # the object was created in the above method
        #ut = Utils()
        self.ut.assert_list_item_text(all_stops, stops)

    #With the data driver testing the 2 stops were implemented using the above test case by passing the multiple values
    # def test_search_flights_2_stop(self):
    #     search_flights_result = self.yatra_launch_page_object.consolidated_search_flights("Bengaluru","Montreal","August 10th")
    #     self.yatra_launch_page_object.page_scroll()
    #     search_flights_result.filter_flights_by_stops("2 Stop")
    #     all_stops = search_flights_result.get_search_flight_results()
    #     self.log.info(all_stops)
    #     self.ut.assert_list_item_text(all_stops, '2 Stop')



