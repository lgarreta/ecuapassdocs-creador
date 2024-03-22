#!/usr/bin/env python3

import sys

from bot_codebin_base import BotCodebinDoc
from ecuapassdocs.info.ecuapass_utils import Utils


#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv

	ecudocPDFFieldsFile   = args [1]   # PDF with Ecudoc fields
	inputsJsonParamsFile  = args [2]  # JSON with input parameters

	botCodebin = BotCodebinCartaporte (ecudocPDFFieldsFile, inputsJsonParamsFile)
	ecudocJsonFieldsFile = botCodebin.getEmbeddedFieldsFromPDF ()
	botCodebin.createCodebinFieldsFile (ecudocJsonFieldsFile)
	botCodebin.login ("colombia")
	botCodebin.nuevaCartaporte ()

#	# Get embedded fields from document PDF file
#	ecudocJsonFieldsFile  = getEmbeddedFieldsFromPDF (ecudocPDFFieldsFile)
#
#	# Create CODEBIN fields file from Ecudoc fields
#	codebinJsonFieldsFile = createCodebinFieldsFile (ecudocJsonFieldsFile, inputsJsonParamsFile)
#
#	# Open CODEBIN web site and go to create new Cartaporte
#	docForm = codebinOpenForm_NuevaCartaporte ()
#	codebinFillForm_NuevaCartaporte (docForm, codebinJsonFieldsFile)


#----------------------------------------------------------------
#----------------------------------------------------------------
class BotCodebinCartaporte (BotCodebinDoc):
	def __init__ (self, ecudocPDFFieldsFile, inputsJsonParamsFile):
		super().__init__(ecudocPDFFieldsFile, inputsJsonParamsFile)
		self.docType = "CARTAPORTE"

	#-- Overwritten
	def getEcudocFieldValue (self, ecudocFields, fieldEcudoc):
		if "Gastos" in fieldEcudoc:
			fieldName	= fieldEcudoc.split (":")[0]
			rowName		= fieldEcudoc.split (":")[1].split (",")[0]
			colName		= fieldEcudoc.split (":")[1].split (",")[1]
			tablaGastos = ecudocFields [fieldName]["value"]
			value		= self.getValueGastosTable (tablaGastos, rowName, colName)
		else:
			value		= ecudocFields [fieldEcudoc]["content"]
			
		return value

	def getValueGastosTable (self, tabla, firstKey, secondKey):
		try:
			text = tabla [firstKey]["value"][secondKey]["value"]
			value = Utils.getNumber (text)
			#print (f">>> GASTOS: Text: <{text}>. Value: <{value}>")
			return value

		except:
			#print (f"Sin valor en '{firstKey}'-'{secondKey}')")
			#printx (traceback_format_exc())
			return None

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
		gastos ["montor"]	= getValueTabla ("ValorFlete", "MontoRemitente")
		gastos ["moneda1"]	= USD if gastos ["montor"] else None
		gastos ["montod"]	= getValueTabla ("ValorFlete", "MontoDestinatario")
		gastos ["moneda2"]	= USD if gastos ["montod"] else None

		# OTROS:
		gastos ["montor1"]	= getValueTabla ("OtrosGastos", "MontoRemitente")
		gastos ["moneda3"]	= USD if gastos ["montor1"] else None
		gastos ["montod1"]	= getValueTabla ("OtrosGastos", "MontoDestinatario")
		gastos ["moneda4"]	= USD if gastos ["montod1"] else None

		# TOTAL
		gastos ["totalmr"]	= getValueTabla ("Total", "MontoRemitente")
		gastos ["monedat"]	= USD if gastos ["totalmr"] else None
		gastos ["totalmd"]	= getValueTabla ("Total", "MontoDestinatario")
		gastos ["monedat2"] = USD if gastos ["totalmd"] else None
	except:
		Utils.printException ("Obteniendo valores de 'gastos'")
		sys.exit (1)

	return gastos


#-----------------------------------------------------------
#-----------------------------------------------------------
main ()
