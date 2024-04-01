
import json, os, re, sys
from os.path import join

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.contrib.messages import add_message
from django.forms.models import model_to_dict

# For CSRF protection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

# For login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import resolve   # To get calling URLs

# Own imports
from ecuapassdocs.info.resourceloader import ResourceLoader 
#from ecuapassdocs.ecuapassutils.pdfcreator import CreadorPDF 
from .pdfcreator import CreadorPDF 

from .models import Cartaporte, Manifiesto, Declaracion
from .models import CartaporteDoc, ManifiestoDoc, DeclaracionDoc

from appusuarios.models import UsuarioEcuapass
#from .pdfcreator import CreadorPDF

#--------------------------------------------------------------------
#-- Vista para manejar las solicitudes de manifiesto
#--------------------------------------------------------------------
LAST_INPUTVALUES = None
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
		global LAST_INPUTVALUES
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
					  "background_image" : self.background_image,
					  "document_url"    : self.document_type
					 }
		return render (request, self.template_name, contextDic)

	#-------------------------------------------------------------------
	# Used to receive a filled manifiesto form and create a response
	# Get doc number and create a PDF from document values.
	#-------------------------------------------------------------------
	@method_decorator(csrf_protect)
	def post (self, request, *args, **kargs):
		global LAST_INPUTVALUES

		# Get values from html form
		inputValues = self.getInputValuesFromForm (request)		  # Values without CPI number
		button_type = request.POST.get('boton_pdf', '').lower()
		fieldValues = self.getFieldValuesFromInputs (inputValues)
		docNumber	= inputValues ["txt00"]

		if "autosave" in button_type:
			docId, docNumber = self.saveDocumentToDB (inputValues, fieldValues, request.user)
			LAST_INPUTVALUES = inputValues
			return JsonResponse ({"id": docId, 'numero': docNumber}, safe=False)

		elif "original" in button_type or "copia" in button_type:
			if self.isDocumentChanged (inputValues, LAST_INPUTVALUES):
				self.saveDocumentToDB (inputValues, fieldValues, request.user)
				LAST_INPUTVALUES = inputValues

			pdf_response = self.createResponseForOneDocument (inputValues, button_type)
			return pdf_response

		# Create single PDF for main and child documents (Cartaporte + Manifiestos)
		elif "paquete" in button_type:
			pdf_response = self.createResponseForMultiDocument (inputValues, button_type)
			return pdf_response

		elif "clonar" in button_type:
			response_data = {'numero': "CLON"}
			return JsonResponse (response_data, safe=False)

		else:
			print (">>> Error: No se conoce opción del botón presionado:", button_type)

	#-------------------------------------------------------------------
	# Create PDF for 'Cartaporte' plus its 'Manifiestos'
	#-------------------------------------------------------------------
	def createResponseForMultiDocument (self, inputValues, button_type):
		creadorPDF = CreadorPDF (self.document_type)

		# Get inputValues for Cartaporte childs
		id = inputValues ["id"]
		valuesList, typesList = self.getInputValuesForDocumentChilds (self.document_type, id)
		inputValuesList       = [inputValues] + valuesList
		docTypesList          = [self.document_type] + typesList

		# Call PDFCreator 
		outPdfPath = creadorPDF.createMultiPdf (inputValuesList, docTypesList, button_type)

		# Respond with the output PDF
		with open(outPdfPath, 'rb') as pdf_file:
			pdfContent = pdf_file.read()

		# Prepare and return HTTP response for PDF
		pdf_response = HttpResponse (content_type='application/pdf')
		pdf_response ['Content-Disposition'] = f'inline; filename="{outPdfPath}"'
		pdf_response.write (pdfContent)

		return pdf_response

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	def getInputValuesForDocumentChilds (self, docType, docId):
		outInputValuesList = []
		outDocTypesList    = []
		try:
			regCartaporte   = Cartaporte.objects.get (id=docId)
			regsManifiestos = Manifiesto.objects.filter (cartaporte=regCartaporte)

			for reg in regsManifiestos:
				docManifiesto  = ManifiestoDoc.objects.get (id=reg.id)
				inputValues = model_to_dict (docManifiesto)
				outInputValuesList.append (inputValues)
				outDocTypesList.append ("MANIFIESTO")
		except modelClass.DoesNotExist:
			print (f"'No existe {docType}' con id '{id}'")

		return outInputValuesList, outDocTypesList

	#-------------------------------------------------------------------
	#-- Create a PDF from document
	#-------------------------------------------------------------------
	def createResponseForOneDocument (self, inputValues, button_type):
		pdf_response = None

		print (">>> Creando respuesta PDF...")
		creadorPDF = CreadorPDF (self.document_type)

		outPdfPath, outJsonPath = creadorPDF.createPdfDocument (inputValues, self.document_type, button_type)

		# Respond with the output PDF
		with open(outPdfPath, 'rb') as pdf_file:
			pdfContent = pdf_file.read()

		# Prepare and return HTTP response for PDF
		pdf_response = HttpResponse (content_type='application/pdf')
		pdf_response ['Content-Disposition'] = f'inline; filename="{outPdfPath}"'
		pdf_response.write (pdfContent)

		return pdf_response

	#-------------------------------------------------------------------
	# Check if document has changed
	#-------------------------------------------------------------------
	def isDocumentChanged (self, inputValues, last_inputValues):
		if last_inputValues == None:
			return True

		for k in inputValues.keys ():
			if last_inputValues [k] != inputValues [k]:
				print ("Diferentes")
				return True

		return False
			
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
			if "boton" in key:
				continue

			inputValues [key] = request.POST [key].replace ("\r\n", "\n")

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
			if fieldName:
				value		 = inputValues [key]
				jsonFieldsDic [fieldName] = {"value": value, "content": value}

		return jsonFieldsDic

	#-------------------------------------------------------------------
	#-- Set saved or default values to inputs
	#-------------------------------------------------------------------
	def setSavedValuesToInputs (self, recordId):
		instanceDoc = None
		if (self.document_type == "cartaporte"):
			instanceDoc = CartaporteDoc.objects.get (id=recordId)
		elif (self.document_type == "manifiesto"):
			instanceDoc = ManifiestoDoc.objects.get (id=recordId)
		elif (self.document_type == "declaracion"):
			instanceDoc = DeclaracionDoc.objects.get (id=recordId)
		else:
			print (f"Error: Tipo de documento '{self.document_type}' no soportado")
			return None

		# Iterating over fields
		for field in instanceDoc._meta.fields:	# Not include "numero" and "id"
			value = getattr (instanceDoc, field.name)
			self.inputParameters [field.name]["value"] = value if value else ""

		return self.inputParameters

	#-------------------------------------------------------------------
	#-- Save document to DB
	#-------------------------------------------------------------------
	def saveDocumentToDB (self, inputValues, fieldValues, username):
		print (">> Guardando documento...")
		docClass, modelClass = self.getDocumentAndModelClass (self.document_type)

		# Create documentDoc and save it to get id
		docNumber = inputValues ["numero"]
		if docNumber == "" or docNumber == "CLON":
			print (">>> Creación de documento nuevo en la BD...")
			documentDoc = docClass ()
			documentDoc.save ()

			# Set values from for to document
			for key, value in inputValues.items():
				if key != "id":
					setattr(documentDoc, key, value)

			# Save initial document form
			documentDoc.numero = self.getDocumentNumber (inputValues, documentDoc.id)
			if documentDoc.txt00:
				documentDoc.numero = documentDoc.txt00
			documentDoc.save ()

			# Save initial document register
			documentModel = modelClass (id=documentDoc.id, numero=documentDoc.numero, documento=documentDoc)
			documentModel.save ()

			self.actualizarNroDocumentosCreados (username, self.document_type)

			return documentDoc.id, documentDoc.numero
		else:
			print (">>> Documento existente en la BD: actualización...")
			docId     = inputValues ["id"]
			docNumber = inputValues ["numero"]
			documentDoc = get_object_or_404 (docClass, id=docId)

			# Assign values to the attributes using dictionary keys
			for key, value in inputValues.items():
				setattr(documentDoc, key, value)
			documentDoc.save ()

			# Retrieve and save Cartaporte register
			documentModel = get_object_or_404 (modelClass, id=docId)
			documentModel.setValues (documentDoc, fieldValues)
			documentModel.save ()

			return docId, docNumber

	#-------------------------------------------------------------------
	# Return form document class and model class from document type
	#-------------------------------------------------------------------
	def getDocumentAndModelClass (self, document_type):
		docClass, modelClass = None, None
		if document_type == "cartaporte":
			docClass, modelClass = CartaporteDoc, Cartaporte
		elif document_type == "manifiesto":
			docClass, modelClass = ManifiestoDoc, Manifiesto
		elif document_type == "declaracion":
			docClass, modelClass = DeclaracionDoc, Declaracion 
		else:
			print (f"Error: Tipo de documento '{document_type}' no soportado")
			sys.exit (0)

		return docClass, modelClass

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

