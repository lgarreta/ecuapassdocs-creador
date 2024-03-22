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

	botCodebin          = BotCodebinCartaporte (ecudocPDFFieldsFile)
	ecudocFields        = botCodebin.getEmbeddedFieldsFromPDF ()
	codebinFields, pais = botCodebin.createCodebinFields (ecudocFields)

	botCodebin.login (pais)
	frameCartaporte   = botCodebin.nuevaCartaporte ()
	botCodebin.fillForm (frameCartaporte, codebinFields)

#----------------------------------------------------------------
# Bot for filling CODEBIN cartaportes from ECUDOCS PDFs
#----------------------------------------------------------------
class BotCodebinCartaporte (BotCodebinDoc):
	def __init__ (self, ecudocPDFFieldsFile):
		super().__init__("CARTAPORTE", "cartaporte_input_parameters.json", ecudocPDFFieldsFile)

	#-- Overwritten: Get value from document field
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

	#-- Get value from Cartaporte Gastos table
	def getValueGastosTable (self, tabla, firstKey, secondKey):
		try:
			text = tabla [firstKey]["value"][secondKey]["value"]
			value = Utils.getNumber (text)
			return value
		except:
			#print (f"Sin valor en '{firstKey}'-'{secondKey}')")
			#printx (traceback_format_exc())
			return None

#-----------------------------------------------------------
#-----------------------------------------------------------
main ()
