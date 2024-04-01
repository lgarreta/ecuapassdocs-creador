#!/usr/bin/env python3

import os, json, sys
from traceback import format_exc as traceback_format_exc

from ecuapassdocs.info.resourceloader import ResourceLoader 
from ecuapassdocs.info.ecuapass_utils import Utils

#---------------------------------------------------------------------
#-- Main
#---------------------------------------------------------------------
USAGE="\n\
Add documents in JSON format (ECUDOCS) to DB \n\
db-add-jsonsToDB.py <document type> <input dir> \n"

def main ():
	args = sys.argv

	if len (args) < 2:
		print (USAGE)
		sys.exit (0)

	docType  = args [1]
	inputDir = args [2]

	#fieldsFilesPath = "inouts/samples-BYZA/cartaportes"
	saveFieldsFilesToDB (docType, inputDir)

#----------------------------------------------------------------
#----------------------------------------------------------------
def saveFieldsFilesToDB (documentType, fieldsFilesPaths):
	# Set django setup
	import django
	sys.path.append ("../..")
	os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "appdocs_main.settings") #appdocs_main") #/settings")
	sys.path.append (f"{os.getcwd()}")
	django.setup ()

	# Get doc fields
	jsonsFiles = [x for x in os.listdir (fieldsFilesPaths) if "DOCFIELDS.json" in x]
	jsonsPaths = [f"{fieldsFilesPaths}/{x}" for x in jsonsFiles ]

	print ("OUT jsons:", jsonsPaths)
	if input ("Continue y/N: ") != "y":
		sys.exit (0)

	#-- Save document fields to Document forms in DB
	for fieldsFile in jsonsPaths:
		fieldsParams = json.load (open (fieldsFile))
		inputsParams = setInputValuesFromDocFieldsFile (documentType, fieldsParams)

		outJsonFile = fieldsFile.split (".")[0] + "-REBUILD.json"
		json.dump (inputsParams, open (outJsonFile, "w"), indent=4)

		print ("\n-- Saving into DB doc: ", os.path.basename (fieldsFile))
		saveDocumentToDB (documentType, inputsParams, fieldsParams, username="admin")

#---------------------------------------------------------------------
#-- Add document to ecuapassdocsdb
#---------------------------------------------------------------------
def saveDocumentToDB (documentType, inputsParams, fieldsParams, username):
	from appdocs.models import Cartaporte, CartaporteDoc, Manifiesto, ManifiestoDoc
	try:
		docClass, regClass = getDocumentRegisterClassesForDocument (documentType)

		# Save Cartaporte document
		docNumber   = inputsParams ["txt00"]["value"]
		if docClass.objects.filter (numero=docNumber).exists():
			print (f"ALERTA: Documento (Doc) con número '{docNumber}' ya existe.")
			return

		# Assign values to the attributes using dictionary keys
		documentDoc = docClass (numero=docNumber)
		try:
			for key, params in inputsParams.items():
				setattr (documentDoc, key, params ["value"])
				documentDoc.save ()
		except:
			print ("-- key:", key)
			print ("-- field:", params ["field"])
			print ("-- value:", params ["value"])

		# Retrieve and save Cartaporte register
		if regClass.objects.filter (numero=docNumber).exists ():
			print (f"ALERTA: Documento (Reg) con número '{docNumber}' ya existe.")
			return

		documentReg = regClass (numero=docNumber)
		documentReg.setValues (documentDoc, fieldsParams)
		documentReg.save ()
	except:
		print (traceback_format_exc())
		sys.exit (0)

#----------------------------------------------------------------
#-- Get values from cartaporte "gastos" table
#----------------------------------------------------------------
def getValueFromGastosTable (tabla, fieldName):
	firstKey  = fieldName.split (":")[1].split(",")[0]
	secondKey = fieldName.split (",")[1]
	try:
		text  = tabla [firstKey]["value"][secondKey]["value"]
		value = Utils.getNumber (text)
		return value
	except:
		print (f"Sin valor en '{firstKey}'-'{secondKey}'")
		#print (traceback_format_exc())

#----------------------------------------------------------------
#----------------------------------------------------------------
def setInputValuesFromDocFieldsFile (documentType, fieldsParams):
	documentType = documentType.upper()
	if documentType == "CARTAPORTE":
		return setInputValuesForCartaporte (fieldsParams)
	elif documentType == "MANIFIESTO":
		return setInputValuesForManifiesto (fieldsParams)
	elif documentType == "DECLARACION":
		return setInputValuesForDeclaracion (fieldsParams)
	else:
		print (f"Tipo de documento '{documentType}' desconocido")
		sys.exit (0)

def setInputValuesForManifiesto (fieldsParams):
	# Load parameters from package
	inputsParams = ResourceLoader.loadJson ("docs", "manifiesto_input_parameters.json")
	for key in inputsParams.keys ():
		try:
			fieldName	   = inputsParams [key] ["field"]
			if "OriginalCopia" in fieldName:
				pass
			elif "Carga_TipoDescripcion" in fieldName:
				value = fieldsParams [fieldName] ["content"]
			elif "Carga_Tipo" in fieldName:
				tipoCarga  = fieldsParams [fieldName]["content"] 
				value = "X" if "X" in tipoCarga.upper() else ""
			else:
				value = fieldsParams [fieldName]["content"]

			inputsParams [key]["value"] = value
		except:
			print ("-- key:", key)
			print ("-- field Name:", fieldName)
			print ("-- field keys:", fieldsParams.keys())
			print ("-- field params:", fieldsParams [fieldName])
			print (f"ALERTA: Clave '{fieldName}' del Input '{key}' no existe en los campos del documento")
			print (traceback_format_exc())
			sys.exit (0)
			
	return inputsParams

def setInputValuesForCartaporte (fieldsParams):
	# Load parameters from package
	inputsParams = ResourceLoader.loadJson ("docs", "cartaporte_input_parameters.json")
	for key in inputsParams.keys ():
		try:
			fieldName	   = inputsParams [key] ["field"]
			if "Gastos" in fieldName:
				fieldTabla = fieldName.split (":")[0]
				tabla      = fieldsParams [fieldTabla] ["value"]
				value      = getValueFromGastosTable (tabla, fieldName)
			elif "OriginalCopia" in fieldName:
				pass
			else:
				value      = fieldsParams [fieldName]["content"]

			inputsParams [key]["value"]     = value
		except:
			print ("-- key:", key)
			print ("-- fieldName:", fieldName)
			print ("-- fieldParams:", fieldsParams [fieldName])
			print (f"ALERTA: Clave '{fieldName}' del Input '{key}' no existe en los campos del documento")
			print (fieldsParams.keys())
			print (traceback_format_exc())
			sys.exit (0)
			
	return inputsParams
#---------------------------------------------------------------------
#---------------------------------------------------------------------
def getDocumentRegisterClassesForDocument (documentType):
	from appdocs.models import Cartaporte, CartaporteDoc, Manifiesto, ManifiestoDoc
	docClass, regClass = None, None
	if documentType == "cartaporte":
		docClass, regClass = CartaporteDoc, Cartaporte
	elif documentType == "manifiesto":
		docClass, regClass = ManifiestoDoc, Manifiesto
	elif documentType == "declaracion":
		docClass, regClass = DeclaracionDoc, Declaracion 
	else:
		print (f"Error: Tipo de documento '{documentType}' no soportado")
		sys.exit (0)

	return docClass, regClass

#---------------------------------------------------------------------
#-- Main
#---------------------------------------------------------------------
main ()

