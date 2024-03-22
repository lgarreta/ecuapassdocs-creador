#!/usr/bin/env python3

import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#--------------------------------------------------------------------
#--------------------------------------------------------------------
def findFormElements ():
	# Find all form elements
	forms = driver.find_elements_by_tag_name('form')
	# Iterate over each form
	for form in forms:
		# Find all elements within the form
		form_elements = form.find_elements_by_xpath(".//*")
		print(f"Form: {form.get_attribute('outerHTML')}")
		print("Elements within the form:")
		for element in form_elements:
			print(element.get_attribute('outerHTML'))

#--------------------------------------------------------------------
#--------------------------------------------------------------------

# Initialize the Chrome WebDriver
driver = webdriver.Chrome ()

# Navigate to a web page
#driver.get ("http://127.0.0.1:8000")

driver.get ("https://byza.corebd.net/indexb.php?mytoken=a8ec3c4e4f049dd40b4d2a0ed5be8a0c&empresa=GRUPO BYZA SAS")


# Wait for the dynamically created elements to be present
try:
	# Give the page some time to load (adjust as needed)
	driver.implicitly_wait(3)  # Wait 10 seconds

	# Find all elements with the tag name "a" (hyperlinks)
	all_links = driver.find_elements(By.TAG_NAME, "a")

	# Print the text or href attribute of each link (adjust as needed)
	for link in all_links:
		print(link.text)  # Print the link text
		print(link.get_attribute("href"))  # Print the link URL

	print ("-- Clicking on 'Carta Porte' link...")
	iniLink = driver.find_element (By.PARTIAL_LINK_TEXT, "Carta Porte")
	iniLink.click()

	print ("-- Clicking on 'Nuevo' link...")
	iniLink = driver.find_element (By.XPATH, "//a[contains(@href, '1.cpi/nuevo.cpi.php?modo=1')]")
	#form = driver.find_element(By.CSS_SELECTOR, "form")
	iniLink.click()

	print ("-- Locate the subframe using its relative URL...")
	subframe_relative_url = "1.cpi/nuevo.cpi.php?modo=1'"
	subframe = driver.find_element(By.XPATH, f"//iframe[contains(@src, '{subframe_relative_url}')]")

	print ("-- Switch to the subframe...")
	driver.switch_to.frame(subframe)

	print ("-- Now you can find elements within the subframe using XPath..")
	element_in_subframe = driver.find_element(By.XPATH, "//input[@id='nremitente']")

	print ("-- Adding text to remintente..") 
	element_in_subframe.send_keys("Hola")

	a = input ()


	print ("-- Gettin form..")
	#iniLink = driver.find_element (By.XPATH, "//a[contains(@href, '1.cpi/nuevo.cpi.php?modo=1')]")
	form = driver.find_element(By.CSS_SELECTOR, "form")

	a = input ()

	forms = driver.find_elements (By.TAG_NAME, 'form')
	# Iterate over each form
	for form in forms:
		# Find all elements within the form
		form_elements = form.find_elements_by_xpath(".//*")
		print(f"Form: {form.get_attribute('outerHTML')}")
		print("Elements within the form:")
		for element in form_elements:
			print(element.get_attribute('outerHTML'))




	a=input ()
	sys.exit(0)

	# Find an input field by ID and type some text into it
	#http://127.0.0.1:8000/usuarios/login/?next=/usuarios/login/

	# Find an input field by ID and type some text into it
	input_field = driver.find_element (By.ID,"id_username")
	input_field.send_keys ("admin")

	input_field = driver.find_element (By.ID ,"id_password")
	input_field.send_keys ("admin")

	# Submit the search (find button by type)
	submit_button = driver.find_element (By.CLASS_NAME, "btn-primary")
	submit_button.click()

	driver.get ("http://127.0.0.1:8000/documentos/cartaporte/importacion")


	findFormElements ()

#	input_element = WebDriverWait (driver, 30).until(
#		EC.presence_of_element_located ((By.ID, "txt02"))
#	)
#
#	# Once the element is present, interact with it
#	input_element.send_keys ("PE00002")
#
#	a = input ("Press any key to quit... ")

finally:
	# Close the WebDriver
	driver.quit ()

