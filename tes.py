from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--start-maximized")  # Buka browser dalam mode layar penuh

driver = webdriver.Chrome(options=chrome_options)

# driver.get("https://www.google.com/search?q=pelajaran+matematika+kelas+4&rlz=1C1GCEA_enID1040ID1040&oq=pelajaran+ma&gs_lcrp=EgZjaHJvbWUqBwgCEAAYgAQyBwgAEAAYgAQyBggBEEUYOTIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCDMyMzJqMWo3qAIAsAIA&sourceid=chrome&ie=UTF-8")
driver.get("https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3Dbokep%2Bindo%26sca_esv%3D568723682%26rlz%3D1C1GCEA_enID1040ID1040%26ei%3DiKcTZbyADpPXseMPt4GxyAw%26ved%3D0ahUKEwi85Nm48smBAxWTa2wGHbdADMkQ4dUDCBE%26uact%3D5%26oq%3Dbokep%2Bindo%26gs_lp%3DEgxnd3Mtd2l6LXNlcnAiCmJva2VwIGluZG9IqBNQAFjeEHAAeACQAQKYAfAGoAG1FqoBDTcuMi4xLjAuMi4wLjG4AQPIAQD4AQHCAggQLhiKBRiRAsICCxAAGIAEGLEDGIMBwgIEEAAYA8ICBRAuGIAEwgILEC4YigUYsQMYgwHCAhEQLhiKBRixAxiDARjHARivAcICCxAAGIoFGLEDGIMBwgIREC4YgAQYsQMYgwEYxwEY0QPCAggQABiKBRiRAsICFxAuGIoFGJECGJcFGNwEGN4EGN8E2AEBwgILEC4YgAQYsQMYgwHCAggQABiABBixA8ICCxAuGIAEGMcBGK8BwgILEC4YgAQYxwEY0QPCAggQABiKBRixA8ICBRAAGIAEwgIaEC4YgAQYsQMYgwEYlwUY3AQY3gQY3wTYAQHCAgcQABiABBgK4gMEGAAgQYgGAboGBggBEAEYFA%26sclient%3Dgws-wiz-serp&q=EgRncL2DGJek7qgGIjCiLxI2ZaVRK3NwCIlg0QlPfjdxHT3bidk8vHjgciGkAhvxi850fpoKRdPp6E7bVVUyAXJaAUM")
# time.sleep(20)

element_rc = driver.find_element(By.XPATH, "//div[@class='rc-anchor-content']")


teks = driver.find_element(By.XPATH, "/html/body").text

print(teks)