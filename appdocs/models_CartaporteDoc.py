import os, tempfile, json
from datetime import date

from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns

from ecuapassdocs.ecuapassinfo.ecuapass_utils import Utils
from ecuapassdocs.ecuapassinfo.ecuapass_info_cartaporte_BYZA import CartaporteByza

#--------------------------------------------------------------------
# Model Empresa
#--------------------------------------------------------------------
class Empresa (models.Model):
	numeroId     = models.CharField (max_length=50)
	nombre       = models.CharField (max_length=50)
	direccion    = models.CharField (max_length=100)
	ciudad       = models.CharField (max_length=50)
	pais         = models.CharField (max_length=20)
	tipoId       = models.CharField (max_length=20)

	def get_absolute_url(self):
		"""Returns the url to access a particular language instance."""
		return reverse('empresa-detail', args=[str(self.id)])

	def __str__ (self):
		return f"{self.nombre} {self.ciudad}-{self.pais}"
	
#--------------------------------------------------------------------
# Model CartaporteDoc
#--------------------------------------------------------------------
class CartaporteDoc (models.Model):
	numero = models.CharField (max_length=20)
	txt00 = models.CharField (max_length=20, null=True)
	txt01 = models.CharField (max_length=200, null=True)
	txt02 = models.CharField (max_length=200, null=True)
	txt03 = models.CharField (max_length=200, null=True)
	txt04 = models.CharField (max_length=200, null=True)
	txt05 = models.CharField (max_length=200, null=True)
	txt06 = models.CharField (max_length=200, null=True)
	txt07 = models.CharField (max_length=200, null=True)
	txt08 = models.CharField (max_length=200, null=True)
	txt09 = models.CharField (max_length=200, null=True)
	txt10 = models.CharField (max_length=200, null=True)
	txt11 = models.CharField (max_length=200, null=True)
	txt12 = models.CharField (max_length=200, null=True)
	txt13_1 = models.CharField (max_length=200, null=True)
	txt13_2 = models.CharField (max_length=200, null=True)
	txt14 = models.CharField (max_length=200, null=True)
	txt15 = models.CharField (max_length=200, null=True)
	txt16 = models.CharField (max_length=200, null=True)
	txt17_11 = models.CharField (max_length=200, null=True)
	txt17_12 = models.CharField (max_length=200, null=True)
	txt17_13 = models.CharField (max_length=200, null=True)
	txt17_14 = models.CharField (max_length=200, null=True)
	txt17_21 = models.CharField (max_length=200, null=True)
	txt17_22 = models.CharField (max_length=200, null=True)
	txt17_23 = models.CharField (max_length=200, null=True)
	txt17_24 = models.CharField (max_length=200, null=True)
	txt17_31 = models.CharField (max_length=200, null=True)
	txt17_32 = models.CharField (max_length=200, null=True)
	txt17_33 = models.CharField (max_length=200, null=True)
	txt17_34 = models.CharField (max_length=200, null=True)
	txt17_41 = models.CharField (max_length=200, null=True)
	txt17_42 = models.CharField (max_length=200, null=True)
	txt17_43 = models.CharField (max_length=200, null=True)
	txt17_44 = models.CharField (max_length=200, null=True)
	txt18 = models.CharField (max_length=200, null=True)
	txt19 = models.CharField (max_length=200, null=True)
	txt20 = models.CharField (max_length=200, null=True)
	txt21 = models.CharField (max_length=200, null=True)
	txt22 = models.CharField (max_length=200, null=True)
	txt23 = models.CharField (max_length=200, null=True)
	txt24 = models.CharField (max_length=200, null=True)

#	def get_absolute_url(self):
#		"""Returns the url to access a particular language instance."""
#		#return reverse('empresa-detail', args=[str(self.id)])


	def __str__ (self):
		return f"{self.numero}, {self.txt02}, {self.txt03}"
	
	def getNumberFromId (self):
		numero = 2000000+ self.numero 
		numero = f"CI{numero}"
		return (self.numero)
		
#--------------------------------------------------------------------
# Model Cartaporte
#--------------------------------------------------------------------
class Cartaporte (models.Model):
	numero        = models.CharField (max_length=20)
	remitente     = models.ForeignKey (Empresa, on_delete=models.CASCADE, null=True)
	documento     = models.OneToOneField (CartaporteDoc, on_delete=models.CASCADE, null=True)
	fecha_emision = models.DateField (default=date.today)

	def get_absolute_url(self):
		"""Returns the url to access a particular language instance."""
		return reverse('cartaporte-detail', args=[str(self.id)])

	def __str__ (self):
		return f"{self.id}, {self.numero} {self.remitente}"

	def setValues (self, cartaporteDoc, fieldValues):
		print (">>> cartaporteDoc:", cartaporteDoc)
		self.numero     = cartaporteDoc.numero
		self.documento  = cartaporteDoc
		self.remitente  = self.getRemitente (fieldValues)
		
	def getRemitente (self, fieldValues):
		try:
			jsonFieldsPath, runningDir = self.createTemporalJson (fieldValues)
			cartaporteInfo    = CartaporteByza (jsonFieldsPath, runningDir)
			info              = cartaporteInfo.getSubjectInfo ("02_Remitente")
			print (">>> Info:", info)

			if any (value is None for value in info.values()):
				return None
			else:
				empresa, created = Empresa.objects.get_or_create (numeroId=info['numeroId'])

				empresa.nombre    = info ["nombre"]
				empresa.direccion = info ["direccion"]
				empresa.ciudad    = info ["ciudad"]
				empresa.pais      = info ["pais"]
				empresa.tipoId    = info ["tipoId"]
				empresa.numeroId  = info ["numeroId"]

				empresa.save ()
				return empresa
		except:
			Utils.printException (f"Obteniedo info del remitente en el texto")
			return None

	def createTemporalJson (self, fieldValues):
		tmpPath        = tempfile.gettempdir ()
		jsonFieldsPath = os.path.join (tmpPath, f"CARTAPORTE-{self.numero}.json")
		json.dump (fieldValues, open (jsonFieldsPath, "w"))
		return (jsonFieldsPath, tmpPath)
 
	
