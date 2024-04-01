#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


#----------------------------------------------------------------
#-- Create ECUPASSDOCS fields from ECUDOC fields using input parameters
#----------------------------------------------------------------
def setFormFieldsFromJson (docFields):
	try:
		inputsParams = ResourceLoader.loadJson ("docs", self.inputsParametersFile)
		codebinFields = {}
		for key in inputsParams:
			fieldEcudoc   = inputsParams [key]["field"]
			fieldCodebin  = inputsParams [key]["fieldCodebin"]
			if fieldCodebin:
				value = self.getEcudocFieldValue (ecudocFields, fieldEcudoc)
				codebinFields [fieldCodebin] = value

		codigoPais = ecudocFields ["00_Pais"]["value"]
		pais = ""
		if codigoPais == "CO":
			pais = "colombia"
		elif codigoPais == "EC":
			pais = "ecuador"
		else:
			print (f"ALERTA: País con código '{codigoPais}' no existe")
			
		return (codebinFields, pais)
	except Exception as e:
		Utils.printException ("Creando campos de CODEBIN")
		return None


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

# Get the inputs from the document form
form = driver.find_element(By.ID, "forma_pdf")	# Find the form by ID
elements = form.find_elements(By.XPATH, ".//*")  # Find all descendants within the form

for e in elements:
	print (e.tag_name, e.get_attribute ("id"))

# Create file with document fields filled 


txt

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
