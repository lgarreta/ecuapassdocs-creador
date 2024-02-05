import os, tempfile, json
from datetime import date

from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns

from ecuapassdocs.ecuapassinfo.ecuapass_utils import Utils
from ecuapassdocs.ecuapassinfo.ecuapass_info_manifiesto_BYZA import ManifiestoByza

from .models_CartaporteDoc import Cartaporte

#--------------------------------------------------------------------
# Model Conductor
#--------------------------------------------------------------------
class Conductor (models.Model):
	documento        = models.CharField (max_length=20)
	nombre           = models.CharField (max_length=50)
	nacionalidad     = models.CharField (max_length=50)
	licencia         = models.CharField (max_length=50)
	fecha_nacimiento = models.CharField (max_length=50)

	class Meta:
		verbose_name_plural = "Conductores"

	def get_absolute_url(self):
		"""Returns the url to access a particular genre instance."""
		return reverse('conductor-detail', args=[str(self.id)])

	def __str__ (self):
		return f"{self.nombre}"

#--------------------------------------------------------------------
# Model Vehiculo
#--------------------------------------------------------------------
class Vehiculo (models.Model):
	placa       = models.CharField (max_length=50)
	marca       = models.CharField (max_length=100)
	pais        = models.CharField (max_length=20)
	chasis      = models.CharField (max_length=50)
	anho        = models.CharField (max_length=20)

	def get_absolute_url(self):
		"""Returns the url to access a particular language instance."""
		return reverse('vehiculo-detail', args=[str(self.id)])

	def __str__ (self):
		return f"{self.marca}, {self.placa}, {self.pais}"
	
#--------------------------------------------------------------------
# Model ManifiestoDoc
#--------------------------------------------------------------------
class ManifiestoDoc (models.Model):
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
	txt13 = models.CharField (max_length=200, null=True)
	txt14 = models.CharField (max_length=200, null=True)
	txt15 = models.CharField (max_length=200, null=True)
	txt16 = models.CharField (max_length=200, null=True)
	txt17 = models.CharField (max_length=200, null=True)
	txt18 = models.CharField (max_length=200, null=True)
	txt19 = models.CharField (max_length=200, null=True)
	txt20 = models.CharField (max_length=200, null=True)
	txt21 = models.CharField (max_length=200, null=True)
	txt22 = models.CharField (max_length=200, null=True)
	txt23 = models.CharField (max_length=200, null=True)
	txt24 = models.CharField (max_length=200, null=True)
	txt25_1 = models.CharField (max_length=200, null=True)
	txt25_2 = models.CharField (max_length=200, null=True)
	txt25_3 = models.CharField (max_length=200, null=True)
	txt25_4 = models.CharField (max_length=200, null=True)
	txt25_5 = models.CharField (max_length=200, null=True)
	txt26 = models.CharField (max_length=200, null=True)
	txt27 = models.CharField (max_length=200, null=True)
	txt28 = models.CharField (max_length=200, null=True)
	txt29 = models.CharField (max_length=200, null=True)
	txt30 = models.CharField (max_length=200, null=True)
	txt31 = models.CharField (max_length=200, null=True)
	txt32_1 = models.CharField (max_length=200, null=True)
	txt32_2 = models.CharField (max_length=200, null=True)
	txt32_3 = models.CharField (max_length=200, null=True)
	txt32_4 = models.CharField (max_length=200, null=True)
	txt33_1 = models.CharField (max_length=200, null=True)
	txt33_2 = models.CharField (max_length=200, null=True)
	txt34 = models.CharField (max_length=200, null=True)
	txt35 = models.CharField (max_length=200, null=True)
	txt36 = models.CharField (max_length=200, null=True)
	txt37 = models.CharField (max_length=200, null=True)
	txt38 = models.CharField (max_length=200, null=True)
	txt39 = models.CharField (max_length=200, null=True)
	txt40 = models.CharField (max_length=200, null=True)

	def __str__ (self):
		return f"{self.numero}, {self.txt03}"
	
#--------------------------------------------------------------------
# Model Manifiesto
#--------------------------------------------------------------------
class Manifiesto (models.Model):
	numero     = models.CharField (max_length=20)
	vehiculo   = models.ForeignKey (Vehiculo, on_delete=models.DO_NOTHING, related_name='vehiculo', null=True)
	documento  = models.OneToOneField (ManifiestoDoc, on_delete=models.DO_NOTHING, null=True)
	cartaporte = models.ForeignKey(Cartaporte, on_delete=models.RESTRICT, null=True)
	fecha_emision = models.DateField (default=date.today)

	def get_absolute_url(self):
		"""Returns the url to access a particular language instance."""
		return reverse('manifiesto-detail', args=[str(self.id)])

	def __str__ (self):
		return f"{self.numero}, {self.vehiculo}"

	def setValues (self, manifiestoDoc, fieldValues):
		jsonFieldsPath, runningDir = self.createTemporalJson (fieldValues)
		manifiestoInfo             = ManifiestoByza (jsonFieldsPath, runningDir)

		self.numero     = manifiestoDoc.numero
		self.vehiculo   = self.getVehiculo (manifiestoInfo, "vehiculo")
		self.remolque   = self.getVehiculo (manifiestoInfo, "remolque")
		self.cartaporte = self.getCartaporte (manifiestoInfo)
		self.documento  = manifiestoDoc
		
	
	def getCartaporte (self, manifiestoInfo):
		numero = None
		try:
			numero = manifiesto.getNumeroCPIC ()
			record = Cartaporte.objects.get (numero=desired_value)
			return record
		except: 
			print (f"Exepcion: Cartaporte número '{numero}' no encontrado.")
		return None

		
	def getVehiculo (self, manifiestoInfo, vehicleType):
		try:
			info = manifiestoInfo.getVehiculoRemolqueInfo (vehicleType)

			if any (value is None for value in info.values()):
				return None
			else:
				vehiculo, created = Vehiculo.objects.get_or_create (placa=info['placa'])

				vehiculo.marca       = info ["marca"]
				vehiculo.placa       = info ["placa"]
				vehiculo.pais        = info ["pais"]
				vehiculo.chasis      = info ["chasis"]
				vehiculo.anho        = info ["anho"]
				vehiculo.certificado = info ["certificado"]

				vehiculo.save ()
				return vehiculo
		except:
			Utils.printException (f"Obteniedo información del vehiculo.")
			return None

	def createTemporalJson (self, fieldValues):
		tmpPath        = tempfile.gettempdir ()
		jsonFieldsPath = os.path.join (tmpPath, f"MANIFIESTO-{self.numero}.json")
		json.dump (fieldValues, open (jsonFieldsPath, "w"))
		return (jsonFieldsPath, tmpPath)

