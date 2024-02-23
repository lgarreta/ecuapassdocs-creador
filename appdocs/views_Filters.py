
from django.shortcuts import render

#from .models_CartaporteDoc import Cartaporte, CartaporteDoc
from .models import Cartaporte, Manifiesto
from .forms import CartaportesFilterForm, ManifiestosFilterForm

def cartaportes_filter (request):
	cartaportes = Cartaporte.objects.all()
	form  = CartaportesFilterForm (request.GET)
	if form.is_valid():
		numero		  = form.cleaned_data.get('numero')
		fecha_emision = form.cleaned_data.get('fecha_emision')
		vehiculo	  = form.cleaned_data.get('vehiculo')

		if numero:
			cartaportes = cartaportes.filter (numero__icontains=numero)
		if fecha_emision:
			cartaportes = cartaportes.filter (fecha_emision=fecha_emision)
		if vehiculo:
			cartaportes = cartaportes.filter (remitente__icontains=vehiculo)

		for cp in cartaportes:
			print (cp)

	return render(request, 'appdocs/cartaportes_filter.html', {'cartaporte_list': cartaportes, 'form': form})


def manifiestos_filter (request):
	manifiestos = Manifiesto.objects.all()
	form  = ManifiestosFilterForm (request.GET)
	if form.is_valid():
		numero		  = form.cleaned_data.get('numero')
		fecha_emision = form.cleaned_data.get('fecha_emision')
		vehiculo	  = form.cleaned_data.get('vehiculo')

		if numero:
			manifiestos = manifiestos.filter (numero__icontains=numero)
		if fecha_emision:
			manifiestos = manifiestos.filter (fecha_emision=fecha_emision)
		if vehiculo:
			manifiestos = manifiestos.filter (remitente__icontains=vehiculo)

		for cp in manifiestos:
			print (cp)

	return render(request, 'appdocs/manifiestos_filter.html', {'manifiesto_list': manifiestos, 'form': form})

