# forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


# books/forms.py
from django import forms

class CartaportesFilterForm (forms.Form):
	numero		   = forms.CharField(required=False)
	fecha_emision  = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
	remitente	   = forms.CharField(required=False)

	def __init__(self, *args, **kwargs):
		super (CartaportesFilterForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'GET'
		self.helper.layout = Layout(
			Row (
				Column ('numero', css_class='col'),
				Column ('fecha_emision', css_class='col'),
				Column ('remitente', css_class='col'),
				css_class='row'
			),
			Submit ('submit', 'Filtrar', css_class='btn btn-primary')
		)


class ManifiestosFilterForm (forms.Form):
	numero		   = forms.CharField(required=False)
	fecha_emision  = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
	vehiculo	   = forms.CharField(required=False)

	def __init__(self, *args, **kwargs):
		super (ManifiestosFilterForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row (
				Column ('numero', css_class='col'),
				Column ('fecha_emision', css_class='col'),
				Column ('vehiculo', css_class='col'),
				css_class='row'
			),
			Submit ('submit', 'Filtrar', css_class='btn btn-primary')
		)

