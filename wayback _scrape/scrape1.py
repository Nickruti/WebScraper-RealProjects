from selenium import webdriver
import os
import requests
import json
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

#Hide the browser operations
opts = webdriver.ChromeOptions()
opts.headless =True

# Reqested Url for web scraping
print("The url should be in this format: target.com/robots.txt")
user_input = input("Enter url you want scrape from WayBack: ")

#create a driver which will control chrome browser for our program
driver = webdriver.Chrome(executable_path= r"chromedriver.exe")
driver.implicitly_wait(10)

print("Scraping is in progress. Go and have a coffee.... *_*")
#global variable for counter
def foo():
    foo.counter += 1
foo.counter = 0

#parse the data and get the output
def find_keyword():
	keyword = 'Disallow'
	with open('content.json') as json_file:
		line = json_file.readline()
		json_dict = json.loads(line)
		word = json_dict.split('\n')
		res = [idx for idx in word if idx.lower().startswith(keyword.lower())]

		f = open('inter.txt', 'a')
		for i in range(len(res)):
			output = res[i].split(':')
			f.write(output[1].replace('$',''))
			f.write('\n')
		f.close()

#check if the page is redirected
def checkIfRedirection():
    redirText = driver.find_element_by_xpath('/html/body/a').text
    if redirText == 'Go To Page...':
        print ("Redirection")
    return

#read the output on first glance
def reader(req):	
	driver.get(req)
	final = driver.find_element_by_tag_name('pre').text
	with open('content.json', 'w') as outfile:
		json.dump(final, outfile)

	find_keyword()
	foo()

#fetching required text content
def looping_through():
	while True:
	
		try:
				
			icon = driver.find_element_by_xpath('//*[@id="wm-ipp-base"]')
			shadowRoot = driver.execute_script('return arguments[0].shadowRoot', icon)
			path_1 = shadowRoot.find_element_by_tag_name('table').find_element_by_class_name("n")
			path_2 = path_1.find_element_by_class_name("b").find_element_by_tag_name('a')
			path_2.click()
			
			try:
				end_here = driver.find_element_by_class_name('error-page-container').text
				continue

			except NoSuchElementException:
				elem_1 = driver.find_element_by_xpath('/html/body/iframe')


				req_1 = elem_1.get_attribute("src")
				driver.get(req_1)

				# storing the output into file
				with open('links_2.txt', 'a') as outfile:
				   	json.dump(req_1, outfile)
				   	outfile.write('\n')

				reader(req_1)

				driver.implicitly_wait(1)

				#get to previous page
				driver.back()
				time.sleep(1)
				
		except :
			try:
				error = driver.find_element_by_xpath('//*[@id="error"]/p').text
				print(error)
				break
			except:
				continue
			
#Search starts here
def action_on_page(link):
	driver.get('http://web.archive.org/')
	search_form = driver.find_element_by_class_name('rbt-input-hint-container').find_element_by_tag_name('input')

	# User request Input/Url 
	#link = 'https://www.freshworks.com/robots.txt'
	# (u'\ue007') is the enter key pressed
	search_form.send_keys(u'\ue007')
	search_form.send_keys(link)
	search_form.send_keys(u'\ue007')

	result = driver.find_element_by_xpath('//*[@id="react-wayback-search"]/div[2]/span/a[1]')  
	result.send_keys(u'\ue007')

	body = driver.find_element_by_tag_name('body')
	body.send_keys(u'\ue00c')
	driver.implicitly_wait(5)

	redirText = driver.find_element_by_xpath('/html/body/a').text
	if redirText == 'Go To Page...':
		print ("Redirection")
    
	elem = driver.find_element_by_xpath('/html/body/iframe')
	req = elem.get_attribute("src")
	driver.get(req)
	
	# storing the output into file
	with open('links_1.txt', 'w') as outfile:
	   	json.dump(req, outfile)
	   	outfile.write('\n')

	reader(req)
	driver.back()
	driver.implicitly_wait(1)
	looping_through()
	driver.close()
	print('Total links fetched ', foo.counter)

	with open('inter.txt','r+') as result:
	    uniqlines = set(result.readlines())
	    with open('output.txt', 'w') as rmdup:
	        rmdup.writelines(set(uniqlines))
	    result.truncate(0)
	os.remove('inter.txt')

action_on_page(user_input)




