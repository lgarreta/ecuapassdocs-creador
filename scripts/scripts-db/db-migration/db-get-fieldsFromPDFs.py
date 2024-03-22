#!/usr/bin/env python3
"Extract doument fields from PDF documents"

import os, sys 

#---------------------------------------------------------------------
#-- Main
#---------------------------------------------------------------------
def main ():
	args = sys.argv
	#-- Get document fields from pdfs 
	inputDir  = args [1]
	outputDir = f"{os.getcwd()}/{args [2]}"

	outFiles = processPDFdocuments (inputDir)
	print ("OUTPUT FILES:", outFiles)

	moveFiles (outFiles, inputDir, outputDir)

#----------------------------------------------------------------
#----------------------------------------------------------------
def moveFiles (outFiles, inputDir, outputDir):
	createDir (outputDir)
	#os.system (f'mv -f {outputDir} old-{outputDir}')
	#os.system (f"mkdir {outputDir}")
	for files in outFiles:
		cmm1 = f"cp {inputDir}/{files[0]} {outputDir}"
		cmm2 = f"mv {files[1]} {outputDir}"
		cmm3 = f"mv {files[2]} {outputDir}"
		os.system (cmm1)
		os.system (cmm2)
		os.system (cmm3)

#----------------------------------------------------------------
#-- Process PDF documents: 
#----------------------------------------------------------------
def processPDFdocuments (inputPDFsDir):
	from ecuserver import ecuapass_doc as ecudoc
	#from ecuserver import ecuapass_feedback
	#from ecuserver import ecuapass_utils

	runningDir = f"{os.getcwd()}/{inputPDFsDir}"
	pdfsFiles  = [x for x in os.listdir (inputPDFsDir) if "MCI-BYZA" in x and "pdf" in x]
	pdfsPaths  = [f"{runningDir}/{x}" for x in pdfsFiles]
	print ("INPUT PDFS:", pdfsPaths)

	#os.chdir (runningDir)
	outFiles   = []
	for inFile in pdfsPaths:
		print ("\n\n>>> Procesando archivo:", inFile)
		ecuapassFieldsFile, docFieldsFile = ecudoc.mainDoc (inFile, runningDir)
		files = (os.path.basename (inFile), ecuapassFieldsFile, docFieldsFile)
		outFiles.append (files)

	return (outFiles)

#----------------------------------------------------------------
#----------------------------------------------------------------
def createDir (dir):
	def checkExistingDir (dir):
		if os.path.lexists (dir):
			headDir, tailDir = os.path.split (dir)
			oldDir = os.path.join (headDir, "old-" + tailDir)
			if os.path.lexists (oldDir):
					checkExistingDir (oldDir)

			os.rename (dir, oldDir)
	checkExistingDir (dir)
	os.system ("mkdir %s" % dir)
#----------------------------------------------------------------
#----------------------------------------------------------------
main ()

