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

#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv

	ecudocPDFFieldsFile  = args [1]   # PDF with Ecudoc fields
	inputsJsonParamsFile  = args [2]  # JSON with input parameters

	# Get embedded fields from document PDF file
	ecudocJsonFieldsFile  = getEmbeddedFieldsFromPDF (ecudocPDFFieldsFile)

	# Create CODEBIN fields file from Ecudoc fields
	codebinJsonFieldsFile = createCodebinFiedsFile (ecudocJsonFieldsFile, inputsJsonParamsFile)

	# Open CODEBIN web site and go to create new Cartaporte
	docForm = codebinOpenForm_NuevaCartaporte ()
	codebinFillForm_NuevaCartaporte (docForm, codebinJsonFieldsFile)

#----------------------------------------------------------------
# Fill CODEBIN fields with ECUDOC fields
#----------------------------------------------------------------
def codebinFillForm_NuevaCartaporte (docForm, codebinJsonFieldsFile):
	codebinFields = json.load (open (codebinJsonFieldsFile))
	for name in codebinFields.keys():
		value = codebinFields [name]

		elem = docForm.find_element (By.NAME, name)
		elem.send_keys (value.replace ("\r\n", "\n"))
	
#----------------------------------------------------------------
# Open browser, login with pais, Menu cartaporte, Nueva, Fill data
#----------------------------------------------------------------
def codebinOpenForm_NuevaCartaporte ():
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
	docSelect.select_by_value ("colombia")
	submit_button = loginForm.find_element (By.XPATH, "//input[@type='submit']")
	submit_button.click()

	print ("-- Clicking on 'Carta Porte' link...")
	iniLink = driver.find_element (By.PARTIAL_LINK_TEXT, "Carta Porte")
	iniLink.click()

	print ("-- Clicking on 'Nuevo' link...")
	iniLink = driver.find_element (By.XPATH, "//a[contains(@href, '1.cpi/nuevo.cpi.php?modo=1')]")
	iniLink.click()

	# Switch to the frame or window containing the <object> element
	object_frame = driver.find_element (By.TAG_NAME, "object")
	wait = WebDriverWait(driver, 3)  # Adjust the timeout as needed
	wait.until (EC.frame_to_be_available_and_switch_to_it (object_frame))

	docForm = driver.find_element (By.TAG_NAME, "form")

	return docForm

#----------------------------------------------------------------
#-- Create CODEBIN json fields file from ECUDOC fields file
#-- Match betwen CODEBIN and ECUDOC fields are in input parameters
#----------------------------------------------------------------
def createCodebinFiedsFile (ecudocJsonFieldsFile, inputsJsonParamsFile):
	try:
		inputsParams = json.load (open (inputsJsonParamsFile))
		ecudocFields = json.load (open (ecudocJsonFieldsFile))

		codebinFields = {}
		GASTOS_PROCESSED = False
		for key in inputsParams:
			try:
				fieldEcudoc  = inputsParams [key]["field"]
				fieldCodebin = inputsParams [key]["fieldCodebin"]

				if fieldCodebin:
					if "Gastos" in fieldEcudoc:
						if not GASTOS_PROCESSED:
							codebinFields = getGastosInfo (ecudocFields, codebinFields)
							GASTOS_PROCESSED = True
					else:
						value = ecudocFields [fieldEcudoc]["content"]
						codebinFields [fieldCodebin] = value
			except:
				print (f"-- Key: {key}")
				print (f"-- Ecudoc Field: {fieldEcudoc}")
				print (f"-- Codebia Fieldn: {fieldCodebin}\n")
				print ("ALERTA: Problema en alguna clave al recorrer los campos de Ecudoc y Codebin") 

		fieldsCodebinFile = ecudocJsonFieldsFile.replace (".json", "-CODEBIN.json")
		json.dump (codebinFields, open (fieldsCodebinFile, "w"), indent=4)

		return (fieldsCodebinFile)
	except:
		Utils.printException ("Creando campos de CODEBIN")
		return None

#-----------------------------------------------------------
#-----------------------------------------------------------
def setDocFields (fieldCodebin, fieldEcudoc, codebinFields, ecudocFields):

def setCartaporteFields (fieldCodebin, fieldEcudoc, codebinFields, ecudocFields):
	if "Gastos" in fieldEcudoc:
		if not GASTOS_PROCESSED:
			codebinFields = getGastosInfo (ecudocFields, codebinFields)
			GASTOS_PROCESSED = True
	else:
		value = ecudocFields [fieldEcudoc]["content"]

#-----------------------------------------------------------
# Get 'gastos' info: monto, moneda, otros gastos
# WARNING: Incomplete, not "seguro" values taken into account
#-----------------------------------------------------------
def getGastosInfo (ecudocFields, codebinFields ):
	#-- Local: Return value from table or None ------
	def getValueTabla (firstKey, secondKey):
		try:
			text = tabla [firstKey]["value"][secondKey]["value"]
			value = Utils.getNumber (text)
			#print (f">>> GASTOS: Text: <{text}>. Value: <{value}>")
			return value

		except:
			print (f"Sin valor en '{firstKey}'-'{secondKey}')")
			#printx (traceback_format_exc())
			return None
	#--------------------------------------------------
	try:
		tabla = ecudocFields ["17_Gastos"]["value"]
		gastos = codebinFields
		USD = "USD"

		# VALOR FLETE: Rem|MonRem|Des|MonDes 
		gastos ["montor"]   = getValueTabla ("ValorFlete", "MontoRemitente")
		gastos ["moneda1"]  = USD if gastos ["montor"] else None
		gastos ["montod"]   = getValueTabla ("ValorFlete", "MontoDestinatario")
		gastos ["moneda2"]  = USD if gastos ["montod"] else None

		# OTROS:
		gastos ["montor1"]  = getValueTabla ("OtrosGastos", "MontoRemitente")
		gastos ["moneda3"]  = USD if gastos ["montor1"] else None
		gastos ["montod1"]  = getValueTabla ("OtrosGastos", "MontoDestinatario")
		gastos ["moneda4"]  = USD if gastos ["montod1"] else None

		# TOTAL
		gastos ["totalmr"]  = getValueTabla ("Total", "MontoRemitente")
		gastos ["monedat"]  = USD if gastos ["totalmr"] else None
		gastos ["totalmd"]  = getValueTabla ("Total", "MontoDestinatario")
		gastos ["monedat2"] = USD if gastos ["totalmd"] else None
	except:
		Utils.printException ("Obteniendo valores de 'gastos'")
		sys.exit (1)

	return gastos

#----------------------------------------------------------------
#-- Get embedded document fields info from PDF document
#----------------------------------------------------------------
def getEmbeddedFieldsFromPDF (pdfPath):
	fieldsJsonPath = pdfPath.replace (".pdf", "-FIELDS.json")
	try:
		with open(pdfPath, 'rb') as pdf_file:
			pdf_reader = PyPDF2.PdfReader(pdf_file)

			# Assuming the hidden form field is added to the first page
			first_page = pdf_reader.pages[0]

			# Extract the hidden form field value 
			text     = first_page.extract_text()  
			jsonText = re.search ("Embedded_jsonData: ({.*})", text).group(1)

			print ("Obteniendo campos desde el archivo PDF...")
			fieldsJsonDic  = json.loads (jsonText)

			json.dump (fieldsJsonDic, open (fieldsJsonPath, "w"), indent=4, sort_keys=True)
	except Exception as e:
		Utils.printException ("No se pudo leer campos embebidos en el documento PDF.")
		return None

	return (fieldsJsonPath)

#----------------------------------------------------------------
#-- Main
#----------------------------------------------------------------
main ()
