from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models_CartaporteDoc import Empresa, Cartaporte, CartaporteDoc
from .models_ManifiestoDoc import Conductor, Vehiculo, Manifiesto, ManifiestoDoc


def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_empresas = Empresa.objects.all().count()
    num_conductors = Conductor.objects.all().count()
    num_vehiculos = Vehiculo.objects.all().count()
    num_cartaportes = Cartaporte.objects.all().count()
    num_manifestos = Manifiesto.objects.all().count()
    
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_empresas':num_empresas,'num_conductors':num_conductors,'num_vehiculos':num_vehiculos,'num_cartaportes':num_cartaportes, 'num_manifiestos':num_manifestos,'num_visits': num_visits},
    )

from django.views import generic

#--------------------------------------------------------------------
#-- Empresa
#--------------------------------------------------------------------
class EmpresaListView(generic.ListView):
    model = Empresa

class EmpresaDetailView(generic.DetailView):
    model = Empresa
    
#--------------------------------------------------------------------
#-- Vehiculo
#--------------------------------------------------------------------
class VehiculoListView(generic.ListView):
    model = Vehiculo

class VehiculoDetailView(generic.DetailView):
    model = Vehiculo

class ManifiestoListView(generic.ListView):
    model = Manifiesto

class ManifiestoDetailView(generic.DetailView):
    model = Manifiesto

# Decorador personalizado para requerir autenticación en una vista basada en clase
def login_required_class(view_func):
    return method_decorator(login_required, name='dispatch')(view_func)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#--------------------------------------------------------------------
#-- Empresa
#--------------------------------------------------------------------
class EmpresaCreate(login_required_class(CreateView)):
    model = Empresa
    fields = '__all__'

class EmpresaUpdate(login_required_class(UpdateView)):
    model = Empresa
    fields = ['tipoId','nombre','direccion','ciudad', 'pais']

class EmpresaDelete(login_required_class(DeleteView)):
    model = Empresa
    success_url = reverse_lazy('empresas')


#--------------------------------------------------------------------
#-- Vehiculo
#--------------------------------------------------------------------
class VehiculoCreate(login_required_class(CreateView)):
    model = Vehiculo
    fields = '__all__'

class VehiculoUpdate(login_required_class(UpdateView)):
    model = Vehiculo
    fields = ['pais','marca','chasis','anho']

class VehiculoDelete(login_required_class(DeleteView)):
    model = Vehiculo
    success_url = reverse_lazy('vehiculos')

#--------------------------------------------------------------------
#-- Conductor
##--------------------------------------------------------------------
class ConductorListView(generic.ListView):
    model = Conductor

class ConductorDetailView(generic.DetailView):
	model = Conductor

class ConductorCreate(login_required_class(CreateView)):
    model = Conductor
    fields = '__all__'

class ConductorUpdate(login_required_class(UpdateView)):
    model = Conductor
    fields = ['nombre','nacionalidad','licencia','fecha_nacimiento']

class ConductorDelete(login_required_class(DeleteView)):
    model = Conductor
    success_url = reverse_lazy('conductors')

#--------------------------------------------------------------------
#-- Cartaporte
#--------------------------------------------------------------------
#class CartaporteDocDetailView(generic.DetailView):
#    model = Cartaporte

class CartaporteListView(generic.ListView):
    model = Cartaporte

class CartaporteDetailView(generic.DetailView):
    model = Cartaporte

class CartaporteCreate(login_required_class(CreateView)):
    model = Cartaporte
    fields = '__all__'

class CartaporteDoc(login_required_class(UpdateView)):
    model = Cartaporte
    fields = '__all__'
    #fields = ['tipo','remitente','destinatario','fecha_emision']

class CartaporteUpdate(login_required_class(UpdateView)):
    model = Cartaporte
    fields = '__all__'
    #fields = ['tipo','remitente','destinatario','fecha_emision']

class CartaporteDelete(login_required_class(DeleteView)):
    model = Cartaporte
    success_url = reverse_lazy('cartaportes')

#--------------------------------------------------------------------
#-- Manifiesto
#--------------------------------------------------------------------
class ManifiestoCreate(login_required_class(CreateView)):
    model = Manifiesto
    fields = '__all__'

class ManifiestoUpdate(login_required_class(UpdateView)):
    model = Manifiesto
    fields = ['vehiculo', 'cartaporte']

class ManifiestoDelete(login_required_class(DeleteView)):
    model = Manifiesto
    success_url = reverse_lazy('manifiestos')


from django.views import View

class InfoView(View):
    template_name = 'info_view.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
