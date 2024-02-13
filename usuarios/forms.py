# from django import forms
# from .models import CustomUser
# from django.contrib.auth.forms import UserCreationForm

# class RegistrationForm (UserCreationForm):
#	  email = forms.EmailField (required=True)
#	  class Meta:
#		  model = CustomUser
#		  fields = ['username', 'email', 'user_type', 'password1', 'password2']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import CustomUser

class RegistrationForm (UserCreationForm):
	email = forms.EmailField (required=False, widget=forms.EmailInput (attrs={'class': 'form-control'}))
	password1 = forms.CharField (
		label="Clave",
		widget=forms.PasswordInput (attrs={'class': 'form-control', 'id': 'password-input'}),
		help_text=password_validation.password_validators_help_text_html (),
	)
	password2 = forms.CharField (
		label="Confirme la Clave",
		widget=forms.PasswordInput (attrs={'class': 'form-control'}),
	)

	# Add an additional field for password strength
	password_strength = forms.CharField (
		widget=forms.HiddenInput (),
		required=False,
	)

	class Meta:
		model = CustomUser
		fields =  ('username', 'email', 'user_type')

	def __init__ (self, *args, **kwargs):
		super().__init__ (*args, **kwargs)
		self.fields ["username"].label = "Usuario"
		self.fields ["email"].label = "Correo"
		self.fields ["user_type"].label = "Tipo de usuario"

