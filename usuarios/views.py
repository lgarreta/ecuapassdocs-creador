from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import CustomUser
from .tables import UserTable


class UserCreate (LoginRequiredMixin, CreateView):
	model = CustomUser
	fields = ['username','email', 'first_name', 'last_name', 'password', 'user_type', 'total_documentos']
	template_name = 'usuarios/user_create.html'
	success_url = reverse_lazy ('listar')

class UserDelete (LoginRequiredMixin, DeleteView):
	model = CustomUser
	template_name = 'usuarios/user_delete.html'
	success_url = reverse_lazy ('listar')

class UserUpdate (LoginRequiredMixin, UpdateView):
	model = CustomUser
	fields = ['username','email', 'first_name', 'last_name', 'password', 'user_type', 'total_documentos']
	template_name = 'usuarios/user_update.html'
	success_url = reverse_lazy ('listar')

#def user_list (request):
#	users = CustomUser.objects.all ()
#	return render (request, 'usuarios/user_list.html', {'users': users})

def user_list(request):
	users = CustomUser.objects.all()
	table = UserTable (users)
	return render(request, 'usuarios/user_list.html', {'table': table})	

def registration (request):
	if request.method == 'POST':
		# Create a form that has request.POST
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			# Set the user's password securely
			username = form.cleaned_data['username']		 
			password1 = form.cleaned_data['password1']
			password2 = form.cleaned_data['password2']

			if password1 == password2:
				user.set_password(password1)
				user.save()
				
				messages.success(request, f'Su cuenta ha sido creada {username} ! Proceda a ingresar')
				return redirect('login')  # Redirect to the login page
			else:
				# Handle password mismatch error here
				form.add_error('password2', 'Claves ingresadas no coinciden')
	else:
		form = RegistrationForm()
	return render(request, 'usuarios/registration.html', {'form': form})

def base (request):
	return render(request, "usuarios/base.html")

def home (request):
	return render(request, "usuarios/home.html")


	
