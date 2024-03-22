#!/usr/bin/env python3

"""
Fill documents into the CODEBIN site using as input an 
ECUAPASSDOCS pdf with their corresponding inputs parameters file
"""
import sys, json, re, time
import PyPDF2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from ecuapassdocs.info.ecuapass_utils import Utils
from ecuapassdocs.info.resourceloader import ResourceLoader 

#----------------------------------------------------------------
#----------------------------------------------------------------
class BotCodebinDoc:
	def __init__ (self, docType, inputsParametersFile, ecudocPDFFieldsFile):
		self.docType              = docType
		self.inputsParametersFile = inputsParametersFile
		self.ecudocPDFFieldsFile  = ecudocPDFFieldsFile

		self.driver = None

	def login (self, pais):
		# Open and click on "Continuar" button
		driver = webdriver.Firefox ()
		driver.get ("https://byza.corebd.net")
		submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
		submit_button.click()

		# Open new window with login form, then switch to it
		window_handles = driver.window_handles
		winMenu = window_handles [-1]
		driver.switch_to.window (winMenu)

		# Login Form : fill user / password
		loginForm = driver.find_element (By.TAG_NAME, "form")
		userInput = loginForm.find_element (By.NAME, "user")
		userInput.send_keys ("GRUPO BYZA")
		pswdInput = loginForm.find_element (By.NAME, "pass")
		pswdInput.send_keys ("GrupoByza2020*")

		# Login Form:  Select pais (Importación or Exportación : Colombia  or Ecuador)
		docSelectElement = driver.find_element (By.XPATH, "//select[@id='tipodoc']")
		docSelect = Select (docSelectElement)
		docSelect.select_by_value (pais)
		submit_button = loginForm.find_element (By.XPATH, "//input[@type='submit']")
		submit_button.click()

		self.driver = driver
		
	def nuevaCartaporte (self):
		print ("-- Clicking on 'Carta Porte' link...")
		iniLink = self.driver.find_element (By.PARTIAL_LINK_TEXT, "Carta Porte")
		iniLink.click()

		print ("-- Clicking on 'Nuevo' link...")
		iniLink = self.driver.find_element (By.XPATH, "//a[contains(@href, '1.cpi/nuevo.cpi.php?modo=1')]")
		iniLink.click()

		# Switch to the frame or window containing the <object> element
		object_frame = self.driver.find_element (By.TAG_NAME, "object")
		wait = WebDriverWait (self.driver, 3)  # Adjust the timeout as needed
		wait.until (EC.frame_to_be_available_and_switch_to_it (object_frame))

		docForm = self.driver.find_element (By.TAG_NAME, "form")

		return docForm

	#----------------------------------------------------------------
	#-- Get embedded document fields info from PDF document
	#----------------------------------------------------------------
	def getEmbeddedFieldsFromPDF (self):
		pdfPath = self.ecudocPDFFieldsFile

		fieldsJsonPath = pdfPath.replace (".pdf", "-FIELDS.json")
		try:
			with open(pdfPath, 'rb') as pdf_file:
				pdf_reader = PyPDF2.PdfReader(pdf_file)

				# Assuming the hidden form field is added to the first page
				first_page = pdf_reader.pages[0]

				# Extract the hidden form field value 
				text	 = first_page.extract_text()  
				jsonText = re.search ("Embedded_jsonData: ({.*})", text).group(1)

				print ("Obteniendo campos desde el archivo PDF...")
				fieldsJsonDic  = json.loads (jsonText)

				json.dump (fieldsJsonDic, open (fieldsJsonPath, "w"), indent=4, sort_keys=True)
		except Exception as e:
			Utils.printException ("No se pudo leer campos embebidos en el documento PDF.")
			return None

		return (fieldsJsonDic)

	#----------------------------------------------------------------
	#-- Create CODEBIN fields from ECUDOC fields using input parameters
	#----------------------------------------------------------------
	def createCodebinFields (self, ecudocFields):
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

	#-----------------------------------------------------------
	# Implemented for each class: get the ECUDOC field value
	#-----------------------------------------------------------
	def getEcudocFieldValue (self, ecudocFields, fieldEcudoc):
		print ("-- Base class: ", fieldEcudoc)
		return ecudocFields [fieldEcudoc]["content"]

	#-----------------------------------------------------------
	#-- Fill CODEBIN form fields with ECUDOC fields
	#-----------------------------------------------------------
	def fillForm (self, docForm, codebinFields):
		#codebinFields = json.load (open (codebinFieldsFile))
		for name in codebinFields.keys():
			value = codebinFields [name]
			if value:
				elem = docForm.find_element (By.NAME, name)
				elem.send_keys (value.replace ("\r\n", "\n"))
		
