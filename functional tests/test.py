from selenium import webdriver
import time
import unittest

class newvisitor(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_title_check_of_homepage(self):
        #he then visits the attendance_genie website 
        self.browser.get("http://localhost:8000")
        assert "Welcome to attendance-genie" in self.browser.title
        #after visiting genie he finds two options
        #1> either to view present attendance statistics
        #2> to submit the attendance record for a particular day(initially let the particular day be today itself)

        #He then clicks on the link to upload attendance statistics for today
        #thereupon he is redirected to a page which contains the subject name, subject code, time slot and two options of attended or 
        #bunked for each of the subject....
        #he then quietly fills up the metrics and clicks on the submit button
        #on submitting he is redirected to the homepage from where he can either upload or view attendance


if __name__=='__main__':
    unittest.main()
