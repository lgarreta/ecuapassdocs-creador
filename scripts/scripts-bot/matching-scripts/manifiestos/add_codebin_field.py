#!/usr/bin/env python3

import os, sys, json

## Add "fieldCodebin" to inputs fields
#inputs = json.load (open ("manifiesto_input_parameters.json"))
#for k in inputs.keys():
#	inputs [k]["fieldCodebin"] = ""
#outFile = "manifiesto_input_parameters-CODEBIN.json"
#json.dump (inputs, open (outFile, "w"), indent=4)

# Show matchs txt : field : fieldCodebin
inputs = json.load (open ("manifiesto_input_parameters-CODEBIN.json"))
for k in inputs.keys():
	txt = k
	field = inputs [k]["field"] 
	fieldCodebin = inputs [k]["fieldCodebin"] 
	print (f" {txt} : {field} : {fieldCodebin}")
