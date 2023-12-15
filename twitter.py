from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--start-maximized")  # Buka browser dalam mode layar penuh

driver = webdriver.Chrome(options=chrome_options)

url = "https://twitter.com"

driver.get(url)
time.sleep(2)

username = "username"
password = "password"

element_signIn = driver.find_element(By.XPATH, "//a[@data-testid='loginButton']")
element_signIn.click()
time.sleep(3.5)
element_input = driver.find_element(By.XPATH, "//input[@name='text']")
element_input.send_keys(username)

element_next = driver.find_element(By.XPATH, "//div[@class='css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu']")
element_next.click()
time.sleep(2)
element_password = driver.find_element(By.XPATH, "//input[@name='password']")
element_password.send_keys(password)
element_login = driver.find_element(By.XPATH, "//div[@data-testid='LoginForm_Login_Button']")
element_login.click()
time.sleep(4)