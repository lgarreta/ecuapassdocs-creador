# forms.py
from django import forms

class NewViewForm(forms.Form):
    campo_1 = forms.CharField(max_length=100)
    campo_2 = forms.CharField(max_length=100)
    # Agrega más campos según sea necesario
