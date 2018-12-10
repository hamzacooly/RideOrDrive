import timer as timer
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.support.ui import WebDriverWait

import time
import unittest

# baseURL = "http://immense-sands-70973.herokuapp.com/"
baseURL = "0.0.0.0:80"

class Test(unittest.TestCase):


    def setUp(self):
        options = Options()
        options.set_headless(True)
        self.browser = webdriver.Chrome('./chromedriver',options=options)

    def test(self):

        self.browser.get(url=baseURL)
        source = self.browser.find_element_by_id("src-field")
        destination = self.browser.find_element_by_id("dst-field")
        submit = self.browser.find_element_by_id("Search")
        source.send_keys("Austin")
        destination.send_keys("Round Rock")
        submit.click()
        wait = WebDriverWait(self.browser, 5)

        try:
            page_loaded = wait.until_not(
                lambda browser: self.browser.current_url == baseURL
            )
        except TimeoutException:
            self.fail("Loading timeout expired")
        second2 = baseURL+"result"
        self.assertTrue(self.browser.current_url==second2,"Successful Search")
        self.assertTrue(self.browser.page_source.__contains__("Your Destination. Your Choice."),"Results displayed")
        print("TEST 1 Results displayed PASSED")



    def test2(self):
        self.browser.get(url=baseURL+"login.html")
        wait = WebDriverWait(self.browser, 5)
        self.assertFalse(self.browser.page_source.__contains__("not found"), "Login page not working")
        print("TEST 2 Login page working PASSED")

    def test3(self):
        self.browser.get(url=baseURL)

        WebDriverWait(self.browser, 1)
        source = self.browser.find_element_by_id("src-field")
        destination = self.browser.find_element_by_id("dst-field")
        submit = self.browser.find_element_by_id("Search")

        source.send_keys("Austin")
        destination.send_keys("Pflugerville")

        submit.click()
        wait=WebDriverWait(self.browser, 10)
        self.assertIsNotNone(self.browser.find_element_by_id('map'))
        print("TEST 3 Map loading PASSED")


    def test4(self):
        self.browser.get(url=baseURL)

        WebDriverWait(self.browser, 1)
        source = self.browser.find_element_by_id("src-field")
        destination = self.browser.find_element_by_id("dst-field")
        submit = self.browser.find_element_by_id("Search")

        source.send_keys("askjnsajkcnsckjsacsa")
        destination.send_keys("sacnskjcnsakjnsax")

        submit.click()
        wait=WebDriverWait(self.browser, 1)
        self.assertIsNotNone(self.browser.find_element_by_id('src-field'))# means that we are on the index page
        print("TEST 4 Invalid Inputs PASSED")

    def test5(self):

        self.browser.get(url=baseURL)

        WebDriverWait(self.browser, 1)
        source = self.browser.find_element_by_id("src-field")
        destination = self.browser.find_element_by_id("dst-field")
        submit = self.browser.find_element_by_id("Search")

        source.send_keys("Austin")
        destination.send_keys("Chicago")

        submit.click()
        wait=WebDriverWait(self.browser, 1)
        uber = self.browser.find_element_by_id('uber')
        self.assertTrue(uber.text is 'Distance too far (>100mi), use Uber client for accurate estimate.',"Uber wonky")
        print("TEST 5 Far destinations PASSED")



    def test6(self):

        self.browser.get(url=baseURL)

        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.url_matches(baseURL))
        source = self.browser.find_element_by_id("src-field")
        destination = self.browser.find_element_by_id("dst-field")
        submit = self.browser.find_element_by_id("Search")

        source.send_keys("Chicago")
        destination.send_keys("400 East 30th Austin")

        submit.click()
        # wait.until(EC.presence_of_element_located('lots'))
        time.sleep(10)
        lots = self.browser.find_element_by_id('lots')
        lots.click()

        self.assertTrue(self.browser.current_url.startswith("https://www.google.com/maps"),"Parking Redirection Didnt work")
        print("TEST 6 Parking redirect PASSED")


    def test7(self):

        self.browser.get(url=baseURL+"static/login.html")
        time.sleep(2)

        wait = WebDriverWait(self.browser, 10)
        username = self.browser.find_element_by_id("username")
        password = self.browser.find_element_by_id("password")
        submit = self.browser.find_element_by_id("signin")

        username.send_keys("student1")
        password.send_keys("something")

        submit.click()
        # wait.until(EC.presence_of_element_located('lots'))


        self.assertTrue(self.browser.current_url.startswith(baseURL)," Correct Login redirection works")
        print("TEST 7 Correct Login redirect PASSED")


    def test8(self):

        self.browser.get(url=baseURL+"static/login.html")

        wait = WebDriverWait(self.browser, 10)
        username = self.browser.find_element_by_id("username")
        password = self.browser.find_element_by_id("password")
        submit = self.browser.find_element_by_id("signin")

        username.send_keys("student1")
        password.send_keys("some")#wrong password

        submit.click()
        # wait.until(EC.presence_of_element_located('lots'))


        self.assertTrue(self.browser.current_url.startswith(baseURL+"submit/login.html")," Correct Wrong Password redirection works")
        print("TEST 8 Correct Wrong Passwrod PASSED")

    def test9(self):

        self.browser.get(url=baseURL+"static/login.html")

        wait = WebDriverWait(self.browser, 10)
        username = self.browser.find_element_by_id("username")
        password = self.browser.find_element_by_id("password")
        submit = self.browser.find_element_by_id("signin")

        username.send_keys("student1234324")
        password.send_keys("some")#

        submit.click()
        # wait.until(EC.presence_of_element_located('lots'))


        self.assertTrue(self.browser.current_url.startswith(baseURL)," Correct Login redirection works")
        print("TEST 9 Correct Login redirect PASSED")

if __name__ == '__main__':
    unittest.main()
    # Test.setUp(unittest.TestCase)
    # Test.test7(unittest.TestCase)