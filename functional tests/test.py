from selenium import webdriver
import time

browser = webdriver.Firefox()
browser.get("http://localhost:8000")
time.sleep(1)
browser.quit()
