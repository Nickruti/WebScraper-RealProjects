from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import os
import json

category = input("Give Selected Category Number :")
driver = webdriver.Chrome(executable_path= r"D:\PythonL\Learning\Webscraper\chromedriver.exe")
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








#for  in driver.find_elements_by_id('exploits-table'):
#   data = [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]
#    print(data)