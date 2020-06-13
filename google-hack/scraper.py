from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import os
import json

print('''----Google Dorks Category----
        1 - Footholds
        2 - Files Containing Usernames
        3 - Sensitive Directories
        4 - Web Server Detection
        5 - Vulnerable Files
        6 - Vulnerable Servers
        7 - Error Messages
        8 - Files Containing Juicy Info
        9 - Files Containing Passwords	
        10 - Sensitive Online Shopping Info
        11 - Network or Vulnerability Data
        12 - Pages Containing Login Portals
        13 - Various Online Devices	
        14 - Advisories and Vulnerabilities''')
category = input("Give Selected Category Number :")
driver = webdriver.Chrome(executable_path= r".\chromedriver.exe")
driver.implicitly_wait(10)
driver.get('https://www.exploit-db.com/google-hacking-database?category='+ category)

time.sleep(2)
path1 = driver.find_elements_by_xpath('//*[@id="exploits-table"]/tbody/tr')
word_list= []
while True:
    try:
        for i in range(1, len(path1)+1):
            path2 = driver.find_element_by_xpath('//*[@id="exploits-table"]/tbody/tr['+ str(i) +']/td[2]/a')
            path2.location_once_scrolled_into_view
            word_list.append(path2.text)
            #print(path2.text)
            time.sleep(0.5)
        nextB = driver.find_element_by_xpath('//*[@id="exploits-table_next"]/a').click()
        time.sleep(2)
    except NoSuchElementException:
        print("Gone through All the pages.")
        break
    except StaleElementReferenceException:
        pass
text_file = open('output.txt','w')
for line in word_list:
    text_file.write(line)
    text_file.write('\n')
driver.close()
