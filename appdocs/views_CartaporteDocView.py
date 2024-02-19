
import json, os, re
from datetime import date
from os.path import join

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

# For CSRF protection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

# Own imports
from ecuapassdocs.ecuapassutils.resourceloader import ResourceLoader 

from .views_EcuapassDocView import EcuapassDocView
from .models_CartaporteDoc import CartaporteDoc, Cartaporte, Empresa

#--------------------------------------------------------------------
#-- Vista para manejar las solicitudes de cartaporte
#--------------------------------------------------------------------
class CartaporteDocView (EcuapassDocView):
	document_type    = "cartaporte"
	template_name    = "doc_forma_cartaporte.html"
	background_image = "appdocs/images/image-cartaporte-vacia-SILOG-BYZA.png"
	parameters_file  = "cartaporte_input_parameters.json"

	def __init__(self, *args, **kwargs):
		self.inputParameters = ResourceLoader.loadJson ("docs", self.parameters_file)
		super().__init__ (self.document_type, self.template_name, self.background_image, 
		                  self.parameters_file, self.inputParameters, *args, **kwargs)
	
	#----------------------------------------------------------------
	#-- Embed fields info (key:value) into PDF doc
	#-- Info is embedded according to Azure format
	#----------------------------------------------------------------
	def getFieldValuesFromBounds (self, inputValues):
		jsonFieldsDic = {}
		gastosDic = {"value": {"ValorFlete":{"value":{}}, 
		                       "Seguro":{"value":{}}, 
							   "OtrosGastos":{"value":{}}, 
							   "Total":{"value":{}}}}

		# Load parameters from package
		cartaporteParametersForInputs = ResourceLoader.loadJson ("docs", self.parameters_file)

		for key, params in cartaporteParametersForInputs.items():
			fieldName    = params ["field"]
			value        = inputValues [key]
			if "Gastos" in fieldName:
				res = re.findall ("\w+", fieldName)   #e.g ["ValorFlete", "MontoDestinatario"]
				tableName, rowName, colName = res [0], res [1], res[2]
				if value != "":
					gastosDic ["value"][rowName]["value"][colName] = {"value": value, "content": value}
			else:
				jsonFieldsDic [fieldName] = {"value": value, "content": value}

		jsonFieldsDic [tableName] = gastosDic
		return jsonFieldsDic

#--------------------------------------------------------------------
#-- Class for autocomplete options while the user is typing
#--------------------------------------------------------------------
# For textarea options
from django.db.models import Q

class CiudadPaisOptionsView (View):
	@method_decorator(csrf_protect)
	def get (self, request, *args, **kwargs):
		query = request.GET.get('query', '')
		ciudadesPaises = ResourceLoader.loadText ("data-cartaportes", "ciudades-paises-colombia-ecuador.txt")
		ciudadesPaises = [x.upper().strip() for x in ciudadesPaises if x.upper().startswith (query)]

		itemOptions = []
		currentDate = self.getFormatedCurrentDate ()
		for i, item in enumerate (ciudadesPaises):
			itemLine = f"{i}. {item}"
			itemText = f"{item}. {currentDate}"
			newItem = {"itemLine" : itemLine, "itemText" : itemText}
			itemOptions.append (newItem)

		return JsonResponse (itemOptions, safe=False)

	def getFormatedCurrentDate (self):
		from datetime import datetime
		spanish_months = { "January": "ENERO", "February": "FEBRERO", "March": "MARZO", "April": "ABRIL",
			"May": "MAYO", "June": "JUNIO", "July": "JULIO", "August": "AGOSTO", "September": "SEPTIEMBRE",
			"October": "OCTUBRE", "November": "NOVIEMBRE", "December": "DICIEMBRE"
		}
		current_time = datetime.now()

		# Format the current time as "YEAR-MONTH-DAY"
		formatted_time = current_time.strftime("%Y-{}-%d").format(spanish_months[current_time.strftime("%B")])

		return (formatted_time)


class EmpresaOptionsView (View):
	@method_decorator(csrf_protect)
	def get (self, request, *args, **kwargs):
		query = request.GET.get('query', '')
		options = Empresa.objects.filter (nombre__istartswith=query).values()

		itemOptions = []
		for i, option in enumerate (options):
			itemLine = f"{i}. {option['nombre']}"
			itemText = "%s\n%s\n%s-%s. %s:%s" % (
			              option ["nombre"], option ["direccion"], 
						  option ["ciudad"], option ["pais"],
						  option ["tipoId"], option ["numeroId"])

			newOption = {"itemLine" : itemLine, "itemText" : itemText}
			itemOptions.append (newOption)

		return JsonResponse (itemOptions, safe=False)


