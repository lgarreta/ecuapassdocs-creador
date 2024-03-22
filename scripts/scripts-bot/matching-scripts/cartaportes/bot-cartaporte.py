#!/usr/bin/env python3

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
driver.get ("http://127.0.0.1:8000")

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

	# Find an input field by ID and type some text into it
	iniLink = driver.find_element (By.LINK_TEXT,"Iniciar sesión")
	iniLink.click()
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

