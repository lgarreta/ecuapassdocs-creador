#!/usr/bin/env python3

"""
Fill documents into the CODEBIN site using as input an 
ECUAPASSDOCS pdf with their corresponding inputs parameters file
"""
import sys, json, re, time, os
import PyPDF2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from ecuapassdocs.info.ecuapass_utils import Utils
from ecuapassdocs.info.resourceloader import ResourceLoader 

#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv

	ecudocsFieldsFile = args [1]   # PDF with Ecudoc fields
	mainCodebinBot ("MANIFIESTO", ecudocsFieldsFile)

#----------------------------------------------------------------
# mainCodebinBot
#----------------------------------------------------------------
def mainCodebinBot (docType, ecudocsFieldsFile):
	botCodebin = CodebinBot (docType, ecudocsFieldsFile)
	botCodebin.start ()

#----------------------------------------------------------------
# Bot for filling CODEBIN forms from ECUDOCS fields info
#----------------------------------------------------------------
class CodebinBot:
	def __init__ (self, docType, ecudocsFieldsFile):
		self.docType           = docType
		self.ecudocsFieldsFile = ecudocsFieldsFile
		self.driver            = None

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	def start (self):
		Utils.printx (">> Transmitiendo '{self.docType}' a ECUAPASSDOCS")
		ecudocsFields = json.load (open (self.ecudocsFieldsFile))
		pais = ecudocsFields.pop ("00_Pais")["content"]
		Utils.printx ("-- pais:", pais)

		self.login (pais)
		if self.docType == "CARTAPORTE":
			frameDocumento = self.nuevoDocumento ("Cartaporte Importación")
		elif self.docType == "MANIFIESTO":
			frameDocumento = self.nuevoDocumento ("Manifiesto Importación")

		#self.fillForm (frameDocumento, ecudocsFields)

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	def login (self, pais):
		driver = webdriver.Chrome ()
		#driver.get ("https://ecuapassdocs-test.up.railway.app/")
		driver.get ("http://127.0.0.1:8000/")

		submit_button = driver.find_element (By.LINK_TEXT, "Iniciar sesión")
		submit_button.click()


		loginForm = driver.find_element (By.TAG_NAME, "form")
		userInput = loginForm.find_element (By.NAME, "username")
		userInput.send_keys ("admin")
		userInput = loginForm.find_element (By.NAME, "password")
		userInput.send_keys ("admin")

		submit_button = loginForm.find_element (By.ID, "submit")
		submit_button.click()

		self.driver = driver
	
	def singleProcess (self):
		driver = webdriver.Chrome ()
		driver.get ("http://127.0.0.1:8000/")
		iniciarSesionLink = driver.find_element (By.LINK_TEXT, "Iniciar sesión")
		iniciarSesionLink.click ()

		# Login with "admin","admin"
		loginForm = driver.find_element (By.TAG_NAME, "form")
		userInput = loginForm.find_element (By.NAME, "username")
		userInput.send_keys ("admin")
		userInput = loginForm.find_element (By.NAME, "password")
		userInput.send_keys ("admin")
		submit_button = loginForm.find_element (By.ID, "submit")
		submit_button.click()

		# Select new document
		link = driver.find_element (By.PARTIAL_LINK_TEXT, "Manifiesto Importación")
		link.click()

		# Get handles of all windows and switch to the new tab
		all_windows = driver.window_handles
		driver.switch_to.window (all_windows[1])

		form = driver.find_element(By.TAG_NAME, "form")	# Find the form by ID

	


		
	
	#-------------------------------------------------------------------
	# Click "Cartaporte"|"Manifiesto" then "Nuevo" returning document frame
	#-------------------------------------------------------------------
	def nuevoDocumento (self, menuString):
		print (">> Documento nuevo")
		try:
			driver = self.driver
			iniLink = driver.find_element (By.PARTIAL_LINK_TEXT, menuString)
			iniLink.click()

			time.sleep (2)

			docForm = driver.find_element (By.TAG_NAME, "form")
			wait = WebDriverWait (driver, 3)  # Create a WebDriverWait object

			self.printAllElements (driver, docForm)
			a = input ("----------------")


			# Wait for all textareas within the form to be present
			textareas = wait.until(
				EC.presence_of_all_elements_located((By.TAG_NAME, "textarea"))
			)

			for textarea in textareas:
				label = textarea.get_attribute("aria-label")  # Get label using aria-label (optional)
				if not label:
					# If no aria-label, try finding the preceding label element (adjust selector if needed)
					label_element = textarea.find_element(By.XPATH, "./preceding-sibling::label[1]")
					label = label_element.text
				value = textarea.get_attribute("value")
				print(f"Textarea Label: {label}\nValue: {value}\n")

			a  = input ("Presione una tecla...")

			print ("-- docForm", docForm)
			ta = docForm.find_element (By.ID, "txt02")
			ta.send_keys ("XXXXXX")

			#self.printAllTextareas (docForm)

			a  = input ("Presione una tecla...")

			linkString = f"//a[contains(@href, '{optionNumber}.{itemString}/nuevo.{itemString}.php?modo=1')]"
			iniLink = driver.find_element (By.XPATH, linkString)
			iniLink.click()

			# Switch to the frame or window containing the <object> element
			object_frame = driver.find_element (By.TAG_NAME, "object")
			wait = WebDriverWait (driver, 2)  # Adjust the timeout as needed
			wait.until (EC.frame_to_be_available_and_switch_to_it (object_frame))

			# Explicitly wait for the form to be located
			docForm = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.TAG_NAME, "form"))
			)

			return docForm
		except Exception as e:
			Utils.printException ("No se pudo crear document nuevo en el CODEBIN")
			return None

	#-----------------------------------------------------------
	#-- Fill CODEBIN form fields with ECUDOC fields
	#-----------------------------------------------------------
	def fillForm (self, docForm, ecudocsFields):
		CARTAPORTE  = self.docType == "CARTAPORTE"
		MANIFIESTO  = self.docType == "MANIFIESTO"
		DECLARACION = self.docType == "DECLARACION"

		for field in ecudocsFields.keys():
			value = ecudocsFields [field]
			if not value:
				continue

			# Reception data copied to the others fields
			if CARTAPORTE and field in ["lugar2", "lugaremision"]:
				continue

			# Radio button group
			elif MANIFIESTO and "radio" in field:
				elem = docForm.find_element (By.ID, field)
				self.driver.execute_script("arguments[0].click();", elem)

			# Tomados de la BD del vehículo y de la BD del conductor
			elif MANIFIESTO and field in ["a9", "a10", "a11", "a12"] and \
				field in ["a19", "a20", "a21", "a22"]:
				continue  

			# Tomados de la BD de la cartaporte
			elif MANIFIESTO and field in ["a29","a30","a31","a32a","a32b",
			                              "a33","a34a","a34b","a34c","a34d","a40"]:
				continue  

			else:
				print ("--- field:", field)
				elem = docForm.find_element (By.NAME, field)
				#elem.click ()
				elem.send_keys (value.replace ("\r\n", "\n"))

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	def printAllLinks (self, driver):
		# Find all elements on the page
		elements = driver.find_elements (By.TAG_NAME, "a")

		# Print the HTML representation of each element
		for element in elements:
			print(element.get_attribute("outerHTML"))

	def printAllTextareas (self, docForm):
		# Find all elements on the page
		elements = docForm.find_elements (By.TAG_NAME, "textarea")

		# Print the HTML representation of each element
		for element in elements:
			print(element.get_attribute("outerHTML"))

	def printAllElements(self, driver, form_id):
		"""
		This function retrieves and prints all elements within a form, including potential dynamic elements.
	  
		Args:
		driver: The Selenium WebDriver instance.
		form_id: The ID of the HTML form.
		"""
		form = driver.find_element(By.ID, form_id)	# Find the form by ID
		print ("---", form)
		elements = form.find_elements(By.XPATH, ".//*")  # Find all descendants within the form
	  
		for element in elements:
			# Skip non-interactive elements or elements without a tag name
			if not element.tag_name or not element.is_displayed() or not element.is_enabled():
			  continue
		  
			# Print element details (tag name, attributes, text content)
			print(f"Tag Name: {element.tag_name}")
			print(f"Attributes: {element.get_attributes()}")  # Dictionary of all attributes
			try:
			  print(f"Text Content: {element.text}")  # Might not be applicable for all elements
			except StaleElementReferenceException:
			  # Handle potential exceptions for dynamic elements
			  print("Element might have changed dynamically.")
			print("-" * 20)


#-----------------------------------------------------------
# Call to main
#-----------------------------------------------------------
if __name__ == "__main__":
	main()
