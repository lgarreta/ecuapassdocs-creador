
import json, os, re, sys
from os.path import join

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.contrib.messages import add_message

# For CSRF protection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

# For login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import resolve   # To get calling URLs

# Own imports
from ecuapassdocs.ecuapassinfo.resourceloader import ResourceLoader 
#from ecuapassdocs.ecuapassutils.pdfcreator import CreadorPDF 
from .pdfcreator import CreadorPDF 

from .models import Cartaporte, Manifiesto, Declaracion
from .models import CartaporteDoc, ManifiestoDoc, DeclaracionDoc

from appusuarios.models import UsuarioEcuapass
#from .pdfcreator import CreadorPDF

#--------------------------------------------------------------------
#-- Vista para manejar las solicitudes de manifiesto
#--------------------------------------------------------------------
class EcuapassDocView (LoginRequiredMixin, View):

	def __init__(self, document_type, template_name, background_image, parameters_file, 
	             inputParameters, *args, **kwargs):
		super().__init__ (*args, **kwargs)
		self.document_type	  = document_type
		self.template_name	  = template_name
		self.background_image = background_image
		self.parameters_file  = parameters_file
		self.inputParameters  = inputParameters

	#-------------------------------------------------------------------
	# Usado para llenar una forma (manifiesto) vacia
	# Envía los parámetros o restricciones para cada campo en la forma de HTML
	#-------------------------------------------------------------------
	def get (self, request, *args, **kwargs):
		self.setInitialValuesToInputs (request)

		# Check if user has reached his total number of documents
		if self.limiteDocumentosAsignados (request.user, self.document_type):
			add_message (request, messages.ERROR, "Límite de documents alcanzado. No puede crear documentos.")
			return render (request, 'messages.html')
			
		# If edit, retrieve the PK from kwargs and load input parameters from package
		pk = kwargs.get ('pk')
		if pk:
			result = self.setSavedValuesToInputs (pk)
			if result == None:
				add_message (request, messages.ERROR, "Tipo de documento desconocido")
				return render (request, 'messages.html')
			
		# Send input fields parameters (bounds, maxLines, maxChars, ...)
		contextDic = {"document_type"	 : self.document_type, 
					  "input_parameters" : self.inputParameters, 
					  "background_image" : self.background_image
					 }
		return render (request, self.template_name, contextDic)

	#-------------------------------------------------------------------
	# Used to receive a filled manifiesto form and create a response
	# Get doc number and create a PDF from document values.
	#-------------------------------------------------------------------
	@method_decorator(csrf_protect)
	def post (self, request, *args, **kargs):

		# Get values from html form
		button_type = request.POST.get('boton_pdf', '').lower()

		inputValues = self.getInputValuesFromForm (request)		  # Values without CPI number
		fieldValues = self.getFieldValuesFromInputs (inputValues)
		docNumber	= inputValues ["txt00"]

		pdfFilename, pdfContent  = self.createPDF  (inputValues, button_type)

		# Prepare and return HTTP response for PDF
		pdf_response = HttpResponse (content_type='application/pdf')
		pdf_response ['Content-Disposition'] = f'inline; filename="{pdfFilename}"'
		pdf_response.write (pdfContent)

		if "preliminar" in button_type:
			return pdf_response
		elif "original" in button_type:
			if docNumber == "" or docNumber == "CLON" or docNumber == "PRELIMINAR": 
				docNumber = self.saveDocumentToDB (inputValues, fieldValues, request.user, "GET-ID")
				return JsonResponse ({'numero': docNumber}, safe=False)
			else: 
				self.saveDocumentToDB (inputValues, fieldValues, request.user, "SAVE-DATA")
				return pdf_response
		elif "copia" in button_type:
			if inputValues ["txt00"] != "":		
				return pdf_response
			else: 
				response_data = {'message': "Error: No se ha creado documento original!" }
				return JsonResponse(response_data, safe=False)
		elif "clonar" in button_type:
			response_data	   = {'numero': "CLON"}
			return JsonResponse (response_data, safe=False)
		else:
			print (">>> Error: No se conoce opción del botón presionado:", button_type)

	#-------------------------------------------------------------------
	#-- Set constant values for the BYZA company
	#-- Overloaded in sublclasses
	#-------------------------------------------------------------------
	def setInitialValuesToInputs (self, request):
		# Importacion/Exportacion code for BYZA
		self.inputParameters ["txt0a"]["value"] = self.getCodigoPaisFromURL (request)

	#-------------------------------------------------------------------
	#-- Get or set codigo pais: CO : importacion or EC : exportacion 
	#-------------------------------------------------------------------
	def getCodigoPaisFromURL (self, request):
		# Try to get previous
		codigoPais = self.inputParameters ["txt0a"]["value"]

		if not codigoPais:
			urlName = resolve(request.path_info).url_name
			if "importacion" in urlName:
				codigoPais = "CO" 
			elif "exportacion" in urlName:
				codigoPais = "EC" 
			else:
				print (f"Alerta: No se pudo determinar código pais desde el URL: '{urlName}'")
				codigoPais = "" 

		return codigoPais
			
	#-------------------------------------------------------------------
	#-- Return a dic with the texts from the document form (e.g. txt00,)
	#-------------------------------------------------------------------
	def getInputValuesFromForm (self, request):
		inputValues = {}
		for key in request.POST:
			if key.startswith ("txt"):
				inputValues [key] = request.POST [key]

		inputValues ["numero"] = inputValues ["txt00"]

		return inputValues

	#----------------------------------------------------------------
	#-- Embed fields info (key:value) into PDF doc
	#-- Info is embedded according to Azure format
	#----------------------------------------------------------------
	def getFieldValuesFromInputs (self, inputValues):
		jsonFieldsDic = {}
		# Load parameters from package
		inputParameters = ResourceLoader.loadJson ("docs", self.parameters_file)
		for key, params in inputParameters.items():
			fieldName	 = params ["field"]
			value		 = inputValues [key]
			jsonFieldsDic [fieldName] = {"value": value, "content": value}

		return jsonFieldsDic

	#-------------------------------------------------------------------
	#-- Set saved or default values to inputs
	#-------------------------------------------------------------------
	def setSavedValuesToInputs (self, recordId):
		docRecord = None
		if (self.document_type == "cartaporte"):
			docRecord = CartaporteDoc.objects.get (id=recordId)
		elif (self.document_type == "manifiesto"):
			docRecord = ManifiestoDoc.objects.get (id=recordId)
		elif (self.document_type == "declaracion"):
			docRecord = DeclaracionDoc.objects.get (id=recordId)
		else:
			print (f"Error: Tipo de documento '{self.document_type}' no soportado")
			return None

		# Iterating over fields
		for field in docRecord._meta.fields [2:]:	# Not include "numero" and "id"
			value = getattr(docRecord, field.name)
			self.inputParameters [field.name]["value"] = value if value else ""

		return self.inputParameters
	#-------------------------------------------------------------------
	#-- Create a PDF from document
	#-------------------------------------------------------------------
	def createPDF (self, inputValues, button_type):
		creadorPDF = CreadorPDF (self.document_type)

		outPdfPath, outJsonPath = creadorPDF.createPdfDocument (inputValues, button_type)

		# Respond with the output PDF
		with open(outPdfPath, 'rb') as pdf_file:
			pdfContent = pdf_file.read()

		return (os.path.basename (outPdfPath), pdfContent)

	#-------------------------------------------------------------------
	#-- Save document to DB
	#-------------------------------------------------------------------
	def saveDocumentToDB (self, inputValues, fieldValues, username, flagSave):
		docClass, modelClass = None, None
		if self.document_type == "cartaporte":
			docClass, modelClass = CartaporteDoc, Cartaporte
		elif self.document_type == "manifiesto":
			docClass, modelClass = ManifiestoDoc, Manifiesto
		elif self.document_type == "declaracion":
			docClass, modelClass = DeclaracionDoc, Declaracion 
		else:
			print (f"Error: Tipo de documento '{document_type}' no soportado")
			sys.exit (0)
			
		# Create documentDoc and save it to get id
		if flagSave == "GET-ID":
			# Save Cartaporte document
			documentDoc = docClass ()
			documentDoc.save ()
			documentDoc.numero = self.getDocumentNumber (inputValues, documentDoc.id)
			documentDoc.save ()
			self.actualizarNroDocumentosCreados (username, self.document_type)

			# Save Initial Cartaporte register
			documentModel = modelClass (id=documentDoc.id, numero=documentDoc.numero)
			documentModel.save ()

			return documentDoc.numero
		elif flagSave == "SAVE-DATA":
			# Retrieve instance and save Cartaporte document
			docNumber = inputValues ["txt00"]
			documentDoc = get_object_or_404 (docClass, numero=docNumber)

			# Assign values to the attributes using dictionary keys
			for key, value in inputValues.items():
				setattr(documentDoc, key, value)

			documentDoc.save ()

			# Retrieve and save Cartaporte register
			documentModel = get_object_or_404 (modelClass, numero=docNumber)
			documentModel.setValues (documentDoc, fieldValues)
			documentModel.save ()

			return inputValues

	#-------------------------------------------------------------------
	# Handle assigned documents for "externo" user profile
	#-------------------------------------------------------------------
	#-- Return if user has reached his max number of asigned documents
	def limiteDocumentosAsignados (self, username, document_type):
		user = get_object_or_404 (UsuarioEcuapass, username=username)
		print (f">>> User: '{username}'. '{document_type}'.  Creados: {user.nro_docs_creados}. Asignados: {user.nro_docs_asignados}")
		
		if (user.perfil == "externo" and user.nro_docs_creados	>= user.nro_docs_asignados):
			return True

		return False

	#-- Only for "cartaportes". Retrieve the object from the DB, increment docs, and save
	def actualizarNroDocumentosCreados (self, username, document_type):
		if (document_type != "cartaporte"):
			return

		user = get_object_or_404 (UsuarioEcuapass, username=username)
		user.nro_docs_creados += 1	# or any other value you want to increment by
		user.save()		
	#-------------------------------------------------------------------
	#-- Create a formated document number ranging from 2000000 
	#-- Uses "codigo pais" as prefix (for NTA, BYZA)
	#-------------------------------------------------------------------
	def getDocumentNumber (self, inputValues, id):
		codigoPais = inputValues ["txt0a"]
		numero = f"{codigoPais}{2000000 + id}"
		return (numero)

