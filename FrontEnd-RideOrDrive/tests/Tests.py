from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import unittest

class Test(unittest.TestCase):

    def test(self):

        browser = webdriver.Chrome('./chromedriver')
        browser.get(url="http://127.0.0.1:5000/")

        source = browser.find_element_by_id("autocompleteSource")
        destination = browser.find_element_by_id("autocompleteDestination")
        submit = browser.find_element_by_id("Search")

        source.send_keys("Austin")
        destination.send_keys("Round Rock")

        submit.click()

        wait = WebDriverWait(browser, 5)

        try:
            page_loaded = wait.until_not(
                lambda browser: browser.current_url == "http://127.0.0.1:5000/"
            )
        except TimeoutException:
            self.fail("Loading timeout expired")


        second2 = "http://127.0.0.1:5000/result"
        # self.assertEqual(
        #
        #     first=browser.current_url,
        #     second=second2,
        #     msg="Successful Login"
        # )
        self.assertTrue(browser.current_url==second2,"Successful Search")
        self.assertTrue(browser.page_source.__contains__("Your Destination. Your Choice."),"Results displayed")
        print("TEST 1 PASSED")



    def test2(self):

        browser = webdriver.Chrome('./chromedriver')
        browser.get(url="http://127.0.0.1:5000/login.html")

        # source = browser.find_element_by_id("autocompleteSource")
        # destination = browser.find_element_by_id("autocompleteDestination")
        # submit = browser.find_element_by_id("Search")
        #
        # source.send_keys("Austin")
        # destination.send_keys("Round Rock")
        #
        # submit.click()

        wait = WebDriverWait(browser, 5)
        self.assertTrue(browser.page_source.__contains__("not found"), "Login page not working")
        print("TEST 2 PASSED")

    def test3(self):
        browser = webdriver.Chrome('./chromedriver')
        browser.get(url="http://127.0.0.1:5000/login.html")

        source = browser.find_element_by_id("autocompleteSource")
        destination = browser.find_element_by_id("autocompleteDestination")
        submit = browser.find_element_by_id("Search")

        source.send_keys("Austin")
        destination.send_keys("Pflugerville")

        submit.click()
        WebDriverWait(browser, 1).until(EC.presence_of_element_located(By.ID, 'map'))
        wait = WebDriverWait(browser, 5)
        print("TEST 3 PASSED")

if __name__ == '__main__':
    unittest.main()