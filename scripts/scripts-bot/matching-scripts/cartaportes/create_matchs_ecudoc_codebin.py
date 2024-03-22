#!/usr/bin/env python3

import os, sys, json

#--------------------------------------------------------------------
# matchFilename contains group of three values: txt : ecuField : binField
#--------------------------------------------------------------------
def main ():
	#createCartaporteMatchFiles ()
	matchFilename    = "inputs_matchs_ecudoc_codebin.txt"
	cartaporteInputsFilename = "cartaporte_input_parameters.json"
	addCodebinFieldsToEcudocFields (matchFilename, cartaporteInputsFilename)

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def addCodebinFieldsToEcudocFields (matchFilename, cartaporteInputsFilename):
	inputs = json.load (open (cartaporteInputsFilename))
	for line in open (matchFilename):
		key   = line.split (" : ")[0].strip()
		fcbin = line.split (" : ")[2].strip()

		inputs [key]["fieldCodebin"] = fcbin 

	outFilename = cartaporteInputsFilename.split (".")[0] + "-CODEBIN.json"
	outFile     = json.dump (inputs, open (outFilename, "w"), indent=4, sort_keys=True)
		

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def createCartaporteMatchFiles ():
	inputsCodebinFile = "cartaporte_inputs_codebin.txt"
	#inputsEcudocsFile = "cartaporte_input_parameters.json"
	inputsEcudocsFile = "cartaporte_inputs_ecudocs.txt"

	inputsCodebin = open (inputsCodebinFile).readlines()
	inputsEcudocs = open (inputsEcudocsFile).readlines()
	#inputsEcudocs = json.load (open (inputsEcudocsFile))
	#inputsEcudocs = json.load (open (inputsEcudocsFile))

	matchLines = []
	for i, line in enumerate (inputsEcudocs):
		try:
			txt   = line.split (" : ")[1].strip()
			field = line.split (" : ")[2].strip()
			fcbin = inputsCodebin [i].strip()
			line = f"{txt} : {field} : {fcbin}"
			matchLines.append (line)
		except:
			pass
	
	matchFilename = "inputs_matchs_ecudoc_codebin.txt", "w"
	matchFile     = open (matchFilename)
	matchFile.writelines ("\n".join (matchLines))
	return matchFilename

#--------------------------------------------------------------------
#--------------------------------------------------------------------
main ()
