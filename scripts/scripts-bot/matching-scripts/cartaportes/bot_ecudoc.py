#!/usr/bin/env python3

import sys, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
#--------------------------------------------------------------------
#--------------------------------------------------------------------
driver = webdriver.Chrome ()
URL_CartaporteImport = "https://ecuapassdocs-test.up.railway.app/documentos/cartaporte/importacion"
driver.get (URL_CartaporteImport)


submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
submit_button.click()

window_handles = driver.window_handles
winMenu = window_handles [1]
driver.switch_to.window (winMenu)

loginForm = driver.find_element (By.TAG_NAME, "form")
userInput = loginForm.find_element (By.NAME, "user")
userInput.send_keys ("GRUPO BYZA")
pswdInput = loginForm.find_element (By.NAME, "pass")
pswdInput.send_keys ("GrupoByza2020*")

docSelectElement = driver.find_element (By.XPATH, "//select[@id='tipodoc']")
docSelect = Select (docSelectElement)
submit_button = loginForm.find_element (By.XPATH, "//input[@type='submit']")
submit_button.click()

# Switch to the frame or window containing the <object> element
object_frame = driver.find_element(By.TAG_NAME, "object")
driver.switch_to.frame(object_frame)

docForm = driver.find_element (By.TAG_NAME, "form")



print ("-- Clicking on 'Carta Porte' link...")
iniLink = driver.find_element (By.PARTIAL_LINK_TEXT, "Carta Porte")
iniLink.click()

print ("-- Clicking on 'Nuevo' link...")
iniLink = driver.find_element (By.XPATH, "//a[contains(@href, '1.cpi/nuevo.cpi.php?          modo=1')]")
iniLink.click()
a = input ()
sys.exit ()


# Navigate to a web page
#driver.get ("http://127.0.0.1:8000")

driver.get ("https://byza.corebd.net")
print ("-- Navigate to the frame containing the form")
driver.get ('https://byza.corebd.net/1.cpi/nuevo.cpi.php?modo=1')


# Wait for the dynamically created elements to be present
try:
	# Give the page some time to load (adjust as needed)
	driver.implicitly_wait(2)  # Wait 10 seconds

#	# Find all elements with the tag name "a" (hyperlinks)
#	all_links = driver.find_elements(By.TAG_NAME, "a")
#
#	# Print the text or href attribute of each link (adjust as needed)
#	for link in all_links:
#		print(link.text)  # Print the link text
#		print(link.get_attribute("href"))  # Print the link URL

	print ("-- Clicking on 'Carta Porte' link...")
	iniLink = driver.find_element (By.PARTIAL_LINK_TEXT, "Carta Porte")
	iniLink.click()

	print ("-- Clicking on 'Nuevo' link...")
	iniLink = driver.find_element (By.XPATH, "//a[contains(@href, '1.cpi/nuevo.cpi.php?modo=1')]")
	iniLink.click()

	print ("-- Navigate to the frame containing the form")
	driver.get ('https://byza.corebd.net/1.cpi/nuevo.cpi.php?modo=1')
	time.sleep (3)

	textFields = driver.find_elements (By.TAG_NAME, "textarea")
	for i, field in enumerate (textFields):
		print (f"Textarea {i} : {field.get_attribute ('name')}")

	inputFields = driver.find_elements (By.TAG_NAME, "input")
	for i, field in enumerate (inputFields):
		print (f"Input {i} : {field.get_attribute ('name')}")

	a = input ()

	print ("-- Waiting to the frame containing the form")
	subframe_relative_url = "/1.cpi/nuevo.cpi.php?modo=1"
	wait = WebDriverWait(driver, 3)  # Adjust the timeout as needed
	#wait.until(EC.frame_to_be_available_and_switch_to_it ((By.XPATH, f"//iframe[contains(@src, '/1.cpi/nuevo.cpi.php?modo=1')]")))

	print ("-- Locate the subframe using its relative URL...")
	subframe_relative_url = "1.cpi/nuevo.cpi.php?modo=1"
	subframe = driver.find_element(By.XPATH, f"//iframe[contains(@src, '/1.cpi/nuevo.cpi.php?modo=1')]")

	print ("-- Switch to the subframe...")
	driver.switch_to.frame(subframe)

	a = input ()

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

